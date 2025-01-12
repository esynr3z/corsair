"""Tests enumeration of a bitfield."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

import corsair as csr

from .utils import build_enum, build_enum_member

# All tests below can be used in smoke testing
pytestmark = pytest.mark.smoke


def test_validation_success() -> None:
    """Test successful validation."""
    member = build_enum_member()
    assert member.name == "ok"
    assert member.doc == "Indicates status is OK"
    assert member.value == 0
    assert isinstance(member.metadata, csr.ItemMetadata)


def test_invalid_value() -> None:
    """Test invalid negative value."""
    with pytest.raises(ValidationError, match="Input should be greater than or equal to 0"):
        build_enum_member(value=-1)


def test_width() -> None:
    """Test width of a member."""
    assert build_enum_member(value=0b111).width == 3
    assert build_enum_member(value=0).width == 1
    assert build_enum_member(value=0b10101010).width == 8


def test_enum_width() -> None:
    """Test width of an enumeration."""
    assert (
        build_enum(
            (
                build_enum_member(name="E1", value=0b1),
                build_enum_member(name="E2", value=0b101),
            )
        ).width
        == 3
    )


def test_enum_iter() -> None:
    """Test iterating over enumeration."""
    enum = build_enum(
        (
            build_enum_member(name="e1", value=1),
            build_enum_member(name="e2", value=2),
            build_enum_member(name="e3", value=3),
        )
    )
    assert tuple(enum.names) == ("e1", "e2", "e3")
    assert tuple(enum.values) == (1, 2, 3)


def test_enum_unique_values() -> None:
    """Test that enumeration member values must be unique."""
    members = (
        build_enum_member(name="ENUM_VALUE_1", value=1),
        build_enum_member(name="ENUM_VALUE_2", value=1),
    )
    with pytest.raises(ValueError, match="enumeration member values are not unique"):
        build_enum(members)


def test_enum_unique_names() -> None:
    """Test that enumeration member names must be unique."""
    members = (
        build_enum_member(name="ENUM_VALUE_1", value=1),
        build_enum_member(name="ENUM_VALUE_1", value=2),
    )
    with pytest.raises(ValueError, match="enumeration member names are not unique"):
        build_enum(members)


def test_enum_members_sorted() -> None:
    """Test that enumeration members are sorted by value."""
    members = (
        build_enum_member(name="ENUM_VALUE_2", value=2),
        build_enum_member(name="ENUM_VALUE_1", value=1),
    )
    build_enum(members)

    build_enum(tuple(sorted(members, key=lambda e: e.value)))


def test_enum_members_assigned_parent() -> None:
    """Test that enum is assigned as parent to every member."""
    members = (
        build_enum_member(name="ENUM_VALUE_1", value=1),
        build_enum_member(name="ENUM_VALUE_2", value=2),
    )
    enum = build_enum(members)
    assert enum.members[0].parent == enum
    assert enum.members[1].parent == enum
