"""CLI command to check user input files."""

from __future__ import annotations

import logging
from enum import Enum
from pathlib import Path
from typing import Annotated, Any

import typer  # noqa: TCH002

import corsair as csr

# Get logger singleton
log = logging.getLogger("corsair")


class _FileType(str, Enum):
    """Input file type based on extension."""

    BUILD = "build"
    """Build specification file (*csrbuild.toml)."""

    MAP_JSON = "json"
    """Register map file in JSON format (*csrmap.json)."""

    MAP_YAML = "yaml"
    """Register map file in YAML format (*csrmap.yaml)."""

    MAP_HJSON = "hjson"
    """Register map file in HJSON format (*csrmap.hjson)."""

    MAP_TOML = "toml"
    """Register map file in TOML format (*csrmap.toml)."""

    MAP_PY = "py"
    """Register map file in Python format (*csrmap.py)."""

    def __str__(self) -> str:
        """Return string representation of file type."""
        return self.value


def _get_file_type(file_path: Path) -> _FileType:
    """Determine the file type based on the file name."""
    name = file_path.name
    if name.endswith("csrbuild.toml"):
        return _FileType.BUILD
    if name.endswith("csrmap.yaml"):
        return _FileType.MAP_YAML
    if name.endswith("csrmap.json"):
        return _FileType.MAP_JSON
    if name.endswith("csrmap.hjson"):
        return _FileType.MAP_HJSON
    if name.endswith("csrmap.toml"):
        return _FileType.MAP_TOML
    if name.endswith("csrmap.py"):
        return _FileType.MAP_PY
    raise ValueError(f"Cannot determine file type for '{file_path}'. Unknown or unsupported extension.")


def _find_files_in_cwd() -> list[Path]:
    """Find all supported Corsair files in the current working directory."""
    files: list[Path] = []
    cwd = Path.cwd()

    log.debug("Searching for files in '%s'", cwd)
    for item in cwd.iterdir():
        try:
            if item.is_file() and _get_file_type(item):
                files.append(item)
        except ValueError:
            pass  # Ignore files with unknown or unsupported extensions

    if not files:
        raise FileNotFoundError("No Corsair files found in the current directory.")
    log.info("Found %d Corsair file(s) in the current directory.", len(files))
    return files


def _validate_input_paths(input_paths: list[Path]) -> list[Path]:
    """Validate that provided paths exist and are files."""
    validated_paths: list[Path] = []
    for path in input_paths:
        if not path.exists():
            raise FileNotFoundError(f"Input file not found: '{path}'")
        if not path.is_file():
            raise IsADirectoryError(f"Input path is a directory, not a file: '{path}'")
        validated_paths.append(path)
    return validated_paths


def _get_files_to_check(input_paths: list[Path] | None) -> list[Path]:
    """Determine the final list of files to check."""
    if input_paths:
        log.info("Using provided input paths")
        return _validate_input_paths(input_paths)

    log.info("No input paths provided. Searching for files in the current directory.")
    return _find_files_in_cwd()


def _check_build_spec(file_path: Path) -> None:
    """Check a build specification file."""
    log.debug("Checking build specification file: '%s'", file_path)
    csr.BuildSpecification.from_toml_file(file_path)


def _prepare_map_loader_cfg(file_type: _FileType, input_file: Path) -> csr.LoaderConfig:
    """Prepare loader configuration for map files."""
    cfg_data: dict[str, Any] = {}
    cfg_data["mapfile"] = input_file
    # Map _FileType back to the 'kind' string expected by loaders
    cfg_data["kind"] = file_type.value

    log.debug("Preparing configuration for '%s' loader", file_type.value)
    if file_type in (
        _FileType.MAP_JSON,
        _FileType.MAP_YAML,
        _FileType.MAP_HJSON,
        _FileType.MAP_TOML,
    ):
        return csr.SerializedLoader.Config.model_validate(cfg_data)
    if file_type == _FileType.MAP_PY:
        return csr.PyModuleLoader.Config.model_validate(cfg_data)
    # This should not happen if _get_file_type is correct
    raise ValueError(f"Internal error: unsupported file type for loader configuration: {file_type}")


def _check_register_map(file_path: Path, file_type: _FileType) -> None:
    """Check a register map file."""
    log.debug("Checking register map file: '%s' (type: %s)", file_path, file_type)
    cfg = _prepare_map_loader_cfg(file_type, file_path)
    loader = cfg.loader_cls(config=cfg)
    loader()


def check(
    input_paths: Annotated[
        list[Path] | None,
        typer.Argument(
            help="Path(s) to build/map file(s) to check. "
            "If omitted, checks all supported files in the current directory.",
            show_default=False,
        ),
    ] = None,
) -> None:
    """Check integrity of Corsair input files (build specifications or register maps)."""
    log.debug("cmd check args: input_paths=%s", input_paths)

    log.info("Determining files to check")
    files_to_check = _get_files_to_check(input_paths)

    errors_found = False
    for file_path in files_to_check:
        try:
            log.debug("Checking file: %s", file_path)
            file_type = _get_file_type(file_path)

            if file_type == _FileType.BUILD:
                _check_build_spec(file_path)
            else:
                _check_register_map(file_path, file_type)
            log.info("%s: OK", file_path)

        except Exception as e:  # noqa: BLE001
            log.error("%s: %s", file_path, e)
            errors_found = True

    if errors_found:
        raise RuntimeError("One or more files failed the integrity check.")

    log.info("All files checked successfully.")
