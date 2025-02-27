"""Corsair application entry point."""

from __future__ import annotations

import logging
import os
from pathlib import Path  # noqa: TCH003
from typing import Annotated, Any

import typer

from corsair import VERSION

from .build import build
from .check import check
from .init import init
from .log import init_logging, is_term_dumb_env
from .schema import schema
from .version import version

# Get logger singleton
log = logging.getLogger("corsair")

# Disable URL in Pydantic validation errors
os.environ["PYDANTIC_ERRORS_INCLUDE_URL"] = "0"


class Typer(typer.Typer):
    def __call__(self, *args: Any, **kwargs: Any) -> int:
        try:
            super().__call__(*args, **kwargs)
        except Exception as e:
            if getattr(self, "is_under_debug", False):
                raise
            log.critical(
                "%s\nRun again with -v flag or set environment variable LOG_LEVEL=DEBUG to get more information.",
                e,
            )
            return 1
        else:
            return 0


# Create Typer application. This is also an entry point for the application.
app = Typer(
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
app.command(no_args_is_help=True)(init)
app.command(no_args_is_help=True)(build)
app.command(no_args_is_help=True)(check)
app.command(no_args_is_help=True)(schema)
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


@app.command(hidden=True)
def test_logging() -> None:
    """Hidden command for testing logging configuration."""
    log.critical(":fire:", extra={"markup": True})

    log.debug("I must not fear.")
    log.debug("Fear is the mind-killer.")
    log.info("Fear is the little-death that brings total obliteration.")
    log.info("I will face my fear.")
    log.warning("I will permit it to pass over me and through me.")
    log.error("And when it has gone past, I will turn the inner eye to see its path.")
    log.critical("Where the fear has gone there will be nothing.")
    raise RuntimeError("Only I will remain.")
