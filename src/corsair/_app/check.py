"""CLI command to check user input files."""

from __future__ import annotations

import json
import logging
from enum import Enum
from pathlib import Path  # noqa: TCH003
from typing import Annotated

import typer  # noqa: TCH002

import corsair as csr

# Get logger singleton
log = logging.getLogger("corsair")


class _LoaderKind(str, Enum):
    """Input file loader kind."""

    BUILD = "build"
    """Loader for build specification file."""

    MAP_JSON = "map_json"
    """Loader for map description file in JSON format."""

    MAP_YAML = "map_yaml"
    """Loader for map description file in YAML format."""

    MAP_HJSON = "map_hjson"
    """Loader for map description file in HJSON format."""

    MAP_TOML = "map_toml"
    """Loader for map description file in TOML format."""

    MAP_PY = "map_py"
    """Loader for map description file in Python format."""

    MAP_CUSTOM = "map_custom"
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
        _LoaderKind,
        typer.Option(
            "--loader",
            help="Loader to use to read the input file.",
            show_choices=True,
        ),
    ] = _LoaderKind.BUILD,
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

    # Prepare configuration for the loader
    cfg_data = json.loads(loader_cfg)
    cfg_data["mapfile"] = input_file

    if loader_kind == _LoaderKind.BUILD:
        csr.BuildSpecification.from_toml_file(input_file)
    elif loader_kind in (
        _LoaderKind.MAP_JSON,
        _LoaderKind.MAP_YAML,
        _LoaderKind.MAP_HJSON,
        _LoaderKind.MAP_TOML,
    ):
        cfg = csr.SerializedLoader.Config.model_validate_json(loader_cfg)
        loader = csr.SerializedLoader(config=cfg)
        loader()
    elif loader_kind == _LoaderKind.MAP_PY:
        cfg = csr.PyModuleLoader.Config.model_validate_json(loader_cfg)
        loader = csr.PyModuleLoader(config=cfg)
        loader()
    elif loader_kind == _LoaderKind.MAP_CUSTOM:
        cfg = csr.CustomLoaderConfig.model_validate_json(loader_cfg)
        loader = cfg.loader_cls(config=cfg)
        loader()
    else:
        raise ValueError(f"Unsupported loader kind: {loader_kind}")

    log.info("No errors found")
