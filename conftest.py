"""Configuration for pytest."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import pytest

collect_ignore = ["docs"]


def pytest_configure(config: pytest.Config) -> None:
    """Perform initial configuration."""
    config.addinivalue_line("markers", "smoke: mark test as smoke to run before commiting code")
