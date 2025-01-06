"""CLI commands to initialize a project."""

from __future__ import annotations

import logging

# Get logger singleton
log = logging.getLogger("corsair")


def init() -> None:
    """Initialize a simple project."""
    log.debug("cmd init args: %s", locals())
    raise NotImplementedError("init command is not implemented yet!")
