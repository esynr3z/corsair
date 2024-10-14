"""Application level logger."""

from __future__ import annotations

import logging
import sys
from typing import Any


class _ColorFormatter(logging.Formatter):
    """Record formatter with color support."""

    def __init__(self, *args: tuple[Any], **kwargs: dict[str, Any]) -> None:
        self.use_colors = False
        super().__init__(*args, **kwargs)

        self._reset_code = "\x1b[0m"
        self._color_codes = {
            logging.DEBUG: "\x1b[32m",  # Green
            logging.INFO: "\x1b[34m",  # Cyan
            logging.WARNING: "\x1b[33m",  # Yellow
            logging.ERROR: "\x1b[31m",  # Red
            logging.CRITICAL: "\x1b[41m",  # Red background
        }

    def format(self, record: logging.LogRecord) -> str:
        levelname_color = record.levelname
        msg_color = record.msg

        if self.use_colors:
            color = self._color_codes.get(record.levelno, self._reset_code)
            if record.levelno == logging.INFO:
                msg_color = f"{self._reset_code}{msg_color}"
            else:
                msg_color = f"{msg_color}{self._reset_code}"
            levelname_color = f"{color}{levelname_color}"

        record.levelname = levelname_color
        record.msg = msg_color
        return super().format(record)


def _init_logger(logger: logging.Logger) -> None:
    """Logger init."""
    logger.handlers.clear()
    logger.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler(sys.stderr)
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(_ColorFormatter("%(levelname)s: %(message)s"))
    logger.addHandler(console_handler)


def set_debug(enable: bool) -> None:
    """Set DEBUG verbosity level for the logger."""
    logger = get_logger()

    if enable:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)


def set_color(enable: bool) -> None:
    """Set color mode for the logger."""
    logger = get_logger()

    for handler in logger.handlers:
        if isinstance(handler.formatter, _ColorFormatter):
            handler.formatter.use_colors = enable


def get_logger(name: str = "corsair") -> logging.Logger:
    """Get the package logger."""
    logger = logging.getLogger(name)

    # Create console handler with custom formatting for the first time
    if not logger.hasHandlers():
        _init_logger(logger)

    return logger
