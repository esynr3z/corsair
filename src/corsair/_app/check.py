"""CLI command to check user input files."""

from __future__ import annotations

import json
import logging
from enum import Enum
from pathlib import Path  # noqa: TCH003
from typing import Annotated, Any

import typer  # noqa: TCH002

import corsair as csr

# Get logger singleton
log = logging.getLogger("corsair")


class LoaderKind(str, Enum):
    """Input file loader kind."""

    BUILD = "build"
    """Loader for build specification file."""

    MAP_JSON = "json"
    """Loader for map description file in JSON format."""

    MAP_YAML = "yaml"
    """Loader for map description file in YAML format."""

    MAP_HJSON = "hjson"
    """Loader for map description file in HJSON format."""

    MAP_TOML = "toml"
    """Loader for map description file in TOML format."""

    MAP_PY = "py"
    """Loader for map description file in Python format."""

    MAP_CUSTOM = "custom"
    """Loader for map description file in custom format."""

    def __str__(self) -> str:
        """Return string representation of loader kind."""
        return self.value


def check(
    input_file: Annotated[
        Path,
        typer.Argument(
            help="Path to a build/map file to check.",
            show_default=False,
        ),
    ],
    loader_kind: Annotated[
        LoaderKind,
        typer.Option(
            "--loader",
            help="Loader to use to read the input file.",
            show_choices=True,
        ),
    ] = LoaderKind.BUILD,
    loader_cfg: Annotated[
        str,
        typer.Option(
            "--loader-cfg",
            metavar="JSON_TEXT",
            help="Loader configuration parsed from JSON string. Default loader configuration is used if not provided.",
            show_default=False,
        ),
    ] = "",
) -> None:
    """Check integrity of user input files."""
    log.debug("cmd check args: %s", locals())

    if loader_kind == LoaderKind.BUILD:
        log.info("Loading build specification from TOML file: %s", input_file)
        csr.BuildSpecification.from_toml_file(input_file)
    else:
        log.info("Preparing %s loader", loader_kind.value)
        cfg = _prepare_loader_cfg(loader_kind, input_file, loader_cfg)
        loader = cfg.loader_cls(config=cfg)

        log.info("Loading %s file and validating its content", input_file)
        loader()

    log.info("No errors found")


def _prepare_loader_cfg(loader_kind: LoaderKind, input_file: Path, loader_cfg: str) -> csr.LoaderConfig:
    """Prepare loader configuration."""
    cfg_data: dict[str, Any] = {}

    if loader_cfg:
        log.info("Loading loader configuration from JSON string")
        cfg_data.update(json.loads(loader_cfg))

    cfg_data["mapfile"] = input_file
    cfg_data["kind"] = loader_kind.value

    log.info("Validating configuration for loader")
    if loader_kind in (
        LoaderKind.MAP_JSON,
        LoaderKind.MAP_YAML,
        LoaderKind.MAP_HJSON,
        LoaderKind.MAP_TOML,
    ):
        return csr.SerializedLoader.Config.model_validate(cfg_data)
    if loader_kind == LoaderKind.MAP_PY:
        return csr.PyModuleLoader.Config.model_validate(cfg_data)
    if loader_kind == LoaderKind.MAP_CUSTOM:
        return csr.CustomLoaderConfig.model_validate(cfg_data)
    raise ValueError(f"Unsupported loader kind to load configuration: {loader_kind}")
