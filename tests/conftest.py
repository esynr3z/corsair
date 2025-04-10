"""Configuration for pytest."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import pytest


def pytest_configure(config: pytest.Config) -> None:
    """Perform initial configuration."""
    config.addinivalue_line("markers", "large: test that takes a long time to run")
