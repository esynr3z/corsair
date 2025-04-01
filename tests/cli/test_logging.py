"""Tests for logging options."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import TYPE_CHECKING

import pytest
from typer.testing import CliRunner

from corsair._app.main import app

if TYPE_CHECKING:
    from pathlib import Path

# All tests below can be used in smoke testing
pytestmark = pytest.mark.smoke

runner = CliRunner()


@pytest.fixture
def temp_log_file(tmp_path: Path) -> Path:
    """Create temporary log file."""
    return tmp_path / "test.log"


def test_default_logging() -> None:
    """Test default logging configuration without any options."""
    result = runner.invoke(app, ["test-logging"])
    assert result.exit_code == 1
    verify_log_format(result.output, has_ansi_color=False, has_rich=True)
    verify_log_level(result.output, logging.INFO)


@pytest.mark.parametrize(
    ("flag", "expected_level"),
    [
        ("-v", "DEBUG"),
        ("-vv", "DEBUG"),
        ("-vvv", "DEBUG"),
        ("-q", "WARNING"),
        ("-qq", "ERROR"),
        ("-qqq", "CRITICAL"),
        ("-v -q", "INFO"),
        ("-vv -q", "DEBUG"),
    ],
)
def test_verbosity_control(flag: str, expected_level: str) -> None:
    """Test verbosity control."""
    result = runner.invoke(app, [*flag.split(), "test-logging"])
    assert result.exit_code == 1
    verify_log_format(result.output, has_ansi_color=False, has_rich=True)
    verify_log_level(result.output, getattr(logging, expected_level))


def test_max_quiet() -> None:
    """Test maximum quiet level."""
    result = runner.invoke(app, ["-qqqq", "test-logging"])
    assert result.exit_code == 1
    assert "INFO" not in result.output, "No INFO message is expected"
    assert "WARNING" not in result.output, "No WARNING message is expected"
    assert "ERROR" not in result.output, "No ERROR message is expected"
    assert "DEBUG" not in result.output, "No DEBUG message is expected"
    assert "CRITICAL" not in result.output, "No CRITICAL message is expected"


def test_no_rich() -> None:
    """Test --no-rich option."""
    result = runner.invoke(app, ["--no-rich", "test-logging"])
    assert result.exit_code == 1
    verify_log_format(result.output, has_rich=False, has_ansi_color=True)
    verify_log_level(result.output, logging.INFO)


def test_no_rich_no_color() -> None:
    """Test --no-rich --no-color options."""
    result = runner.invoke(app, ["--no-rich", "--no-color", "test-logging"])
    assert result.exit_code == 1
    verify_log_format(result.output, has_rich=False, has_ansi_color=False)
    verify_log_level(result.output, logging.INFO)


def test_log_file(temp_log_file: Path) -> None:
    """Test logging to file with -l/--log option."""
    result = runner.invoke(app, ["-l", str(temp_log_file), "test-logging"])
    assert result.exit_code == 1
    assert temp_log_file.exists(), "Log file not created"

    content = temp_log_file.read_text()
    verify_log_format(content, has_rich=False, has_ansi_color=False)
    verify_log_level(content, logging.INFO)


# Environment variable tests
def test_env_no_color(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test NO_COLOR environment variable."""
    monkeypatch.setenv("NO_COLOR", "1")
    result = runner.invoke(app, ["--no-rich", "test-logging"])
    assert result.exit_code == 1
    verify_log_format(result.output, has_ansi_color=False, has_rich=False)


def test_env_term_dumb(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test TERM=dumb environment variable."""
    monkeypatch.setenv("TERM", "dumb")
    result = runner.invoke(app, ["test-logging"])
    assert result.exit_code == 1
    verify_log_format(result.output, has_ansi_color=True, has_rich=False)


def test_env_log_level(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test LOG_LEVEL environment variable."""
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")
    result = runner.invoke(app, ["test-logging"])
    assert result.exit_code == 1
    verify_log_level(result.output, logging.DEBUG)


def test_stacktrace_enabled() -> None:
    """Test stacktrace logging is enabled when DEBUG level is set."""
    result = runner.invoke(app, ["-v", "test-logging"])
    assert result.exit_code == 1
    assert result.exception is not None, "Exception should have been caught"
    assert isinstance(result.exception, RuntimeError), "Caught exception should be RuntimeError"
    # Optionally check exc_info for traceback details if needed
    # assert result.exc_info is not None


def test_stacktrace_disabled() -> None:
    """Test stacktrace logging is disabled by default."""
    result = runner.invoke(app, ["test-logging"])
    assert result.exit_code == 1
    assert result.exception is not None, "Exception should have been caught by runner"
    assert isinstance(result.exception, RuntimeError), "Caught exception should be RuntimeError"
    assert "Traceback" not in result.output, "Traceback should not be in the output"


def verify_log_format(
    output: str,
    has_ansi_color: bool = True,
    has_rich: bool = True,
) -> None:
    """Verify log message formatting."""
    assert output, "No output to verify"

    # Check for ANSI color codes
    assert has_ansi_color == ("\x1b[" in output), "Color formatting is expected"

    assert (
        "INFO" in output or "WARNING" in output or "ERROR" in output or "DEBUG" in output or "CRITICAL" in output
    ), "Missing level name"

    if has_rich:
        assert "🔥".encode() in output.encode(), "Missing rich rendered emoji"
    else:
        assert ":fire:" in output, "Emoji should not be rendered!"


def verify_log_level(output: str, min_level: int) -> None:
    """Verify minimum log level in output."""
    assert output, "No output to verify"

    level_messages = {
        logging.DEBUG: " I must not fear",
        logging.INFO: " Fear is the little-death",
        logging.WARNING: " I will permit it to pass over me",
        logging.ERROR: " And when it has gone past",
        logging.CRITICAL: " Where the fear has gone",
    }

    # Check that messages at or above min_level are present
    for level, message in level_messages.items():
        if level >= min_level:
            assert message in output, f"Missing {logging.getLevelName(level)} message"
        else:
            assert message not in output, f"Unexpected {logging.getLevelName(level)} message"
