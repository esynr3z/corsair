"""CLI commands to generate JSON schemas for user input files."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Annotated

import typer  # noqa: TCH002

# Get logger singleton
log = logging.getLogger("corsair")


def schemas(outdir: Annotated[Path, typer.Argument(help="Path for output files.")] = Path()) -> None:
    """Dump JSON schemas for all possible user input files."""
    log.debug("cmd schemas args: %s", locals())
