"""Tests enumeration mode of a bitfield."""

from __future__ import annotations

from typing import Any

import pytest
from pydantic import ValidationError

from corsair import StrictEnumMember

# All tests below can be used in smoke testing
pytestmark = pytest.mark.smoke


def default_member(**kwargs: Any) -> StrictEnumMember:
    """Create default enum member."""
    defaults = {
        "name": "ok",
        "doc": "Indicates status is OK",
        "value": 0,
        "metadata": {},
    }
    defaults.update(kwargs)
    return StrictEnumMember(**defaults)


def test_validation_success() -> None:
    """Test successful validation."""
    member = default_member()
    assert member.name == "ok"
    assert member.doc == "Indicates status is OK"
    assert member.value == 0
    assert isinstance(member.metadata, dict)
    assert len(member.metadata) == 0


def test_invalid_value() -> None:
    """Test invalid negative value."""
    with pytest.raises(ValidationError, match="Input should be greater than or equal to 0"):
        default_member(value=-1)
