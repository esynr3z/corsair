"""CLI commands to generate JSON schemas for user input files."""

from __future__ import annotations

import json
import logging
from enum import Enum
from pathlib import Path  # noqa: TCH003
from typing import TYPE_CHECKING, Annotated

import typer

import corsair as csr

if TYPE_CHECKING:
    from pydantic import BaseModel


# Get logger singleton
log = logging.getLogger("corsair")


class SchemaKind(str, Enum):
    """Schema kind."""

    BUILD = "build"
    """Schema for build specification file."""

    MAP = "map"
    """Schema for map description file."""

    def __str__(self) -> str:
        """Return string representation of schema kind."""
        return self.value


def schema(
    kind: Annotated[SchemaKind, typer.Argument(help="Schema kind.", show_choices=True, show_default=False)],
    indent: Annotated[
        int | None,
        typer.Option(
            "--indent",
            metavar="N",
            help="Indentation level for JSON output. Single line form is used if not provided.",
            show_default=False,
        ),
    ] = None,
    out: Annotated[
        Path | None,
        typer.Option(
            "--out",
            "-o",
            metavar="PATH",
            help="Path for output file. If not provided, then schema is printed to stdout.",
            show_default=False,
        ),
    ] = None,
) -> None:
    """Dump JSON schema for user input file."""
    log.debug("cmd 'schema' args: %s", locals())

    model: type[BaseModel]
    if kind == SchemaKind.BUILD:
        model = csr.BuildSpecification
    elif kind == SchemaKind.MAP:
        model = csr.Map
    else:
        raise ValueError(f"Invalid schema kind: {kind}")

    data = model.model_json_schema()

    if out is None:
        log.info("Schema for %s file is printed to stdout.", kind)
        typer.echo(json.dumps(data, indent=indent))
    else:
        log.info("Schema for %s file is written to %s.", kind, out)
        with out.open("w") as f:
            json.dump(data, f, indent=indent)
