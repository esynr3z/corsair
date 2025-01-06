"""CLI command for printing the application version."""

from __future__ import annotations

import logging

import typer

from corsair import VERSION

# Get logger singleton
log = logging.getLogger("corsair")


def version() -> None:
    """Print the application version."""
    log.debug("Entering version command")
    typer.echo(f"{VERSION}")
