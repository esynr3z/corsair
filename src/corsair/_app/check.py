"""CLI command to check user input files."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Annotated

import typer  # noqa: TCH002

# Get logger singleton
log = logging.getLogger("corsair")


def check(
    spec: Annotated[
        Path,
        typer.Argument(
            help="Path to a build specification file.",
        ),
    ] = Path("corsair.toml"),
) -> None:
    """Check integrity of user input files."""
    log.debug("cmd check args: %s", locals())
    raise NotImplementedError("check command is not implemented yet!")
