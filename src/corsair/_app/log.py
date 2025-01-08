"""Configure logging for Corsair application."""

from __future__ import annotations

import logging
import os
import sys
from typing import TYPE_CHECKING, Any

import typer
from rich.console import Console
from rich.logging import RichHandler

if TYPE_CHECKING:
    from pathlib import Path


class _ColorFormatter(logging.Formatter):
    """Record formatter with color support."""

    def __init__(self, *args: Any, no_color: bool = True, **kwargs: Any) -> None:
        self.no_color = no_color
        super().__init__(*args, **kwargs)

        self._reset_code = "\x1b[0m"
        self._color_codes = {
            logging.DEBUG: "\x1b[32m",  # Green
            logging.INFO: "\x1b[34m",  # Cyan
            logging.WARNING: "\x1b[33m",  # Yellow
            logging.ERROR: "\x1b[1;31m",  # Bold Red
            logging.CRITICAL: "\x1b[41m",  # Red background
        }

    def format(self, record: logging.LogRecord) -> str:
        original_levelname = record.levelname

        levelname_color = record.levelname
        if not self.no_color:
            color = self._color_codes.get(record.levelno, self._reset_code)
            levelname_color = f"{color}{levelname_color}{self._reset_code}"

        record.levelname = levelname_color
        formatted_message = super().format(record)

        # Restore original levelname to avoid breaking other handlers
        record.levelname = original_levelname

        return formatted_message


def _get_format_string(is_debug: bool) -> str:
    """Get format string for the current logging mode."""
    if is_debug:
        return "%(asctime)s: %(levelname)-8s: %(filename)s:%(lineno)d: %(message)s"
    return "%(levelname)-8s: %(message)s"


def _get_logging_level(verbosity_change: int) -> tuple[int, bool]:
    """Determine logging level and debug mode."""
    env_log_level = os.getenv("LOG_LEVEL", "WARNING").upper()
    base_level: int = getattr(logging, env_log_level)
    current_level = base_level - verbosity_change * 10
    is_debug = current_level <= logging.DEBUG

    return current_level, is_debug


def _create_rich_handler(no_color: bool, is_debug: bool) -> logging.Handler:
    """Create RichHandler for logging."""
    formatter = logging.Formatter("%(message)s")
    handler = RichHandler(
        console=Console(stderr=True, no_color=no_color),
        show_time=is_debug,
        show_level=True,
        show_path=is_debug,
        enable_link_path=False,
    )
    handler.setFormatter(formatter)
    return handler


def _create_stream_handler(no_color: bool, is_debug: bool) -> logging.Handler:
    """Create StreamHandler with color formatting."""
    formatter = _ColorFormatter(_get_format_string(is_debug), no_color=no_color)
    handler = logging.StreamHandler(stream=sys.stderr)
    handler.setFormatter(formatter)
    return handler


def _create_file_handler(logfile: Path, is_debug: bool) -> logging.Handler:
    """Create FileHandler for logging to a file."""
    try:
        logfile.parent.mkdir(parents=True, exist_ok=True)
        formatter = logging.Formatter(_get_format_string(is_debug))
        handler = logging.FileHandler(logfile, mode="w", encoding="utf-8")
        handler.setFormatter(formatter)
        handler.setLevel(logging.DEBUG)  # Log everything to file
    except OSError as e:
        # Print error message using typer.echo
        typer.echo(f"Failed to create log file: {e}", err=True)
        raise typer.Exit(code=1) from e
    else:
        return handler


def is_no_color_env() -> bool:
    """Check if NO_COLOR environment variable is set."""
    return bool(os.getenv("NO_COLOR", ""))


def is_term_dumb_env() -> bool:
    """Check if TERM environment variable is set to dumb/unknown."""
    return os.getenv("TERM", "").lower() in ("dumb", "unknown")


def init_logging(
    app: typer.Typer,
    verbosity_change: int,
    no_color: bool,
    no_rich: bool,
    logfile: Path | None = None,
) -> None:
    """Initialize logging."""
    current_level, is_debug = _get_logging_level(verbosity_change)
    if is_debug:
        app.pretty_exceptions_short = False

    # Determine if colors are used (https://no-color.org/)
    no_color = is_no_color_env() or no_color

    # Determine if rich formating is used
    no_rich = is_term_dumb_env() or no_rich
    if no_rich:
        app.pretty_exceptions_enable = False

    handlers = []

    # Create stderr handler
    if no_rich:
        handlers.append(_create_stream_handler(no_color, is_debug))
    else:
        handlers.append(_create_rich_handler(no_color, is_debug))

    # Create file handler if logfile is provided
    if logfile is not None:
        handlers.append(_create_file_handler(logfile, is_debug))

    # Initialize logging with all handlers
    logging.basicConfig(level=current_level, handlers=handlers)
