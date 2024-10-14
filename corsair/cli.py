"""Command-line interface of Corsair."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

from . import utils
from .project import ProjectKind
from .version import __version__


@dataclass
class Args:
    """Application CLI arguments."""

    workdir: Path
    regmap: Path | None
    config: Path | None
    targets: list[str]
    init_project: ProjectKind | None
    debug: bool
    no_color: bool


class ArgumentParser(argparse.ArgumentParser):
    """Corsair CLI argument parser."""

    def __init__(self) -> None:
        """Parser constructor."""
        super().__init__(
            prog="corsair",
            description="Control and status register (CSR) map generator for HDL projects.",
        )

        self.add_argument("-v", "--version", action="version", version=f"%(prog)s v{__version__}")
        self.add_argument(
            "--debug",
            action="store_true",
            dest="debug",
            help="increase logging verbosity level",
        )
        self.add_argument(
            "--no-color",
            action="store_true",
            dest="no_color",
            help="disable use of colors for logging",
        )
        self.add_argument(
            metavar="WORKDIR",
            nargs="?",
            dest="workdir",
            type=Path,
            default=Path(),
            help="working directory (default is the current directory)",
        )
        self.add_argument(
            "-r",
            metavar="PATH",
            dest="regmap",
            type=Path,
            help="register map file",
        )
        self.add_argument(
            "-c",
            "--cfg",
            metavar="PATH",
            type=Path,
            dest="config",
            help="configuration file",
        )
        self.add_argument(
            "-t",
            "--target",
            nargs="*",
            metavar="NAME",
            type=str,
            dest="targets",
            default=[],
            help="make ony selected target(s) from configuration file",
        )
        self.add_argument(
            "-i",
            "--init",
            metavar="KIND",
            type=ProjectKind,
            choices=[k.value for k in ProjectKind],
            dest="init_project",
            help="initialize simple project from template and exit",
        )


def parse_args() -> Args:
    """Parse CLI arguments."""
    parser = ArgumentParser()

    args = parser.parse_args()
    args.workdir = utils.resolve_path(args.workdir)

    return Args(**vars(args))
