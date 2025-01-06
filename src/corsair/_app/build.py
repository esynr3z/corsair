"""CLI command to build output files."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Annotated

import typer  # noqa: TCH002

# Get logger singleton
log = logging.getLogger("corsair")


def build(
    spec: Annotated[
        Path | None,
        typer.Argument(
            show_default=False,
            help="Optional path to a build specification file. "
            "By default, 'csrbuild.toml' or '*.csrbuild.toml' are expected.",
        ),
    ] = Path("csrbuild.toml"),
    targets: Annotated[
        list[str] | None,
        typer.Option(
            "--target",
            "-t",
            metavar="NAME",
            show_default=False,
            help="""Select targets to build.\n
                Option can be applied multiple times.\n
                Special option 'all' can be used to build every target.""",
        ),
    ] = None,
) -> None:
    """Build all the targets according to the provided specification."""
    log.debug("cmd build args: %s", locals())
    if targets is None:
        targets = ["all"]
    raise NotImplementedError("build command is not implemented yet!")
