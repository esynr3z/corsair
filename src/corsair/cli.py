"""CLI of the Corsair application."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Annotated

import typer

from . import input, log, utils
from .version import __version__

# Get loger singleton
logger = log.get_logger()

# Create Typer appication. This is also an entry point for the application.
app = typer.Typer(
    no_args_is_help=True,
    invoke_without_command=True,
    help=f"CorSaiR v{__version__} -- CSR map generator for HDL projects.",
    epilog="""
        Pass --help after any COMMAND to get additional help.\n
        Set DEBUG=1 environment variable to enable verbose output for debugging.\n
        Set NO_COLOR=1 environment variable to disable any color in output.\n
        Set TERM=dumb or TERM=unknown environment variable to enable plain text output (disables colors as well).""",
)

# Disable any color output if user wish
if os.getenv("NO_COLOR"):
    # https://no-color.org/
    log.set_color(False)
    # rich output is uncolorized automatically
else:
    log.set_color(True)

# Disable any rich formated output if user wish (disables color as well)
if os.getenv("TERM") in ("dumb", "unknown"):
    # Values above are from rich package documentation, but for typer we need to apply them manually
    typer.core.rich = None  # pyright: ignore [reportAttributeAccessIssue]
    app.pretty_exceptions_enable = False

# Enable verbose output for debugging if user wish
if os.getenv("DEBUG"):
    app.pretty_exceptions_short = False
    log.set_debug(True)


@app.command()
def build(
    spec: Annotated[
        Path | None,
        typer.Argument(
            show_default=False,
            help="Optional path to a build specification file. "
            "By default, 'crsbuild.toml' or '*.csrbuild.toml' are expected.",
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
    logger.debug("cmd build args: %s", locals())
    if targets is None:
        targets = ["all"]
    raise NotImplementedError("build command is not implemented yet!")


@app.command()
def check(
    spec: Annotated[
        Path,
        typer.Argument(
            help="Path to a build specification file.",
        ),
    ] = Path("corsair.toml"),
) -> None:
    """Check integrity of user input files."""
    logger.debug("cmd check args: %s", locals())
    raise NotImplementedError("check command is not implemented yet!")


@app.command()
def init() -> None:
    """Initialize a simple project."""
    logger.debug("cmd init args: %s", locals())
    raise NotImplementedError("init command is not implemented yet!")


@app.command()
def schemas(outdir: Annotated[Path, typer.Argument(help="Path for output files.")] = Path()) -> None:
    """Dump JSON schemas for all possible user input files."""
    logger.debug("cmd schemas args: %s", locals())
    with utils.chdir(outdir):
        buildspec_schema = outdir / "csrbuild.schema.json"
        logger.info("Dump schema for the build specification: %s", buildspec_schema)
        input.buildspec.BuildSpecification.to_json_schema_file(buildspec_schema)


@app.callback()
def main(
    version: Annotated[
        bool,
        typer.Option("--version", help="Show the application's version and exit."),
    ] = False,
) -> None:
    """CSR map generator for HDL projects."""
    if version:
        typer.echo(f"v{__version__}")
        raise typer.Exit
