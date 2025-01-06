"""Corsair application entry point."""

from __future__ import annotations

import logging
from pathlib import Path  # noqa: TCH003
from typing import Annotated

import typer

from corsair import VERSION

from .build import build
from .check import check
from .init import init
from .log import init_logging, is_term_dumb_env
from .schemas import schemas
from .version import version

# Get logger singleton
log = logging.getLogger("corsair")

# Create Typer application. This is also an entry point for the application.
app = typer.Typer(
    no_args_is_help=True,
    invoke_without_command=True,
    help=f"CorSaiR v{VERSION} -- CSR map generator for HDL projects.",
    context_settings={"help_option_names": ["-h", "--help"]},
    epilog="""
        Pass --help or -h after any COMMAND to get additional help.\n
        Set NO_COLOR=1 environment variable to disable any color in output.\n
        Set TERM=dumb or TERM=unknown environment variable to enable plain text output.""",
)

# Add commands located in other files
app.command()(init)
app.command()(build)
app.command()(check)
app.command()(schemas)
app.command()(version)

if is_term_dumb_env():
    typer.core.rich = None  # pyright: ignore [reportAttributeAccessIssue]


@app.callback()
def main(
    more_verbose: Annotated[
        int,
        typer.Option(
            "--verbose",
            "-v",
            count=True,
            help="Increase verbosity. Can be applied multiple times to increase even more. "
            "Default is WARNING level unless LOG_LEVEL environment variable is set.",
            show_default=False,
        ),
    ] = 0,
    less_verbose: Annotated[
        int,
        typer.Option(
            "--quiet",
            "-q",
            count=True,
            help="Decrease verbosity. Can be applied multiple times to decrease even more."
            "Default is WARNING level unless LOG_LEVEL environment variable is set.",
            show_default=False,
        ),
    ] = 0,
    no_color: Annotated[
        bool,
        typer.Option(
            "--no-color",
            help="Disable color output. "
            "When not provided, color is enabled unless the NO_COLOR environment variable is set.",
            show_default=False,
        ),
    ] = False,
    no_rich: Annotated[
        bool,
        typer.Option(
            "--no-rich",
            help="Disable rich formatting. "
            "When not provided, rich formatting is enabled unless "
            "the TERM environment variable is set to 'dumb' or 'unknown'.",
            show_default=False,
        ),
    ] = False,
    logfile: Annotated[
        Path | None,
        typer.Option("--log", "-l", help="Log file to write to.", show_default=False),
    ] = None,
) -> None:
    """CSR map generator for HDL projects."""
    init_logging(
        app=app,
        verbosity_change=more_verbose - less_verbose,
        no_color=no_color,
        no_rich=no_rich,
        logfile=logfile,
    )
