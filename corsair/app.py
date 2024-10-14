"""Main code of the Corsair application."""

from __future__ import annotations

import sys

from . import log, utils, version
from .cli import Args, parse_args

logger = log.get_logger()

Dummy = int


def main() -> None:
    """Entry point of the application."""
    try:
        app(parse_args())
    except Exception:
        logger.exception("Application finished with error. See the exception description below.")
        sys.exit(1)


def app(args: Args) -> None:
    """Application body."""
    log.set_debug(args.debug)
    log.set_color(not args.no_color)

    logger.debug("corsair v%s", version.__version__)
    logger.debug("args=%s", args)

    with utils.chdir(args.workdir):
        logger.info("Working directory is '%s'", args.workdir)
        if args.init_project:
            create_project(args)
        else:
            globcfg, targets = read_config(args)
            regmap = read_regmap(args, globcfg)
            make_targets(args, globcfg, targets, regmap)


def create_project(args: Args) -> None:
    """Create a simple project, which can be used as a template for user."""
    logger.info("Start creating simple %s project ...", args.init_project)


def read_config(args: Args) -> tuple[Dummy, list[Dummy]]:
    """Read configuration file."""
    logger.debug("args=%s", args)  # TODO: remove when argument is used below
    logger.info("Start reading configuration file ...")
    raise NotImplementedError("read_config() is not implemented!")


def read_regmap(args: Args, globcfg: Dummy) -> Dummy | None:
    """Read register map."""
    logger.debug("args=%s globcfg=%s", args, globcfg)  # TODO: remove when arguments are used below
    logger.info("Start reading register map ...")
    raise NotImplementedError("read_regmap() is not implemented!")


def make_targets(args: Args, globcfg: Dummy, targets: list[Dummy], regmap: Dummy | None) -> None:
    """Make required targets."""
    # TODO: remove when arguments are used below
    logger.debug("args=%s globcfg=%s targets=%s regmap=%s", args, globcfg, targets, regmap)
    logger.info("Start generation ...")
    raise NotImplementedError("make_targets() is not implemented!")
