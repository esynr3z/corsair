"""Tests bitfield."""

from __future__ import annotations

from typing import Any

import pytest

from corsair import Access, Hardware, StrictEnum, StrictEnumMember, StrictField

# All tests below can be used in smoke testing
pytestmark = pytest.mark.smoke


def default_field(**kwargs: Any) -> StrictField:
    """Return a default StrictField instance with optional overrides."""
    defaults = {
        "name": "field_name",
        "doc": "A brief description.\n\nA detailed description of the field.",
        "reset": 0,
        "width": 8,
        "offset": 0,
        "access": Access.RW,
        "hardware": Hardware.NA,
        "enum": None,
        "metadata": {},
    }
    defaults.update(kwargs)
    return StrictField(**defaults)


def test_validation() -> None:
    """Test that a valid StrictField instance can be created."""
    bf = default_field()
    assert isinstance(bf, StrictField)
    assert bf.name == "field_name"
    assert bf.doc == "A brief description.\n\nA detailed description of the field."
    assert bf.reset == 0
    assert bf.width == 8
    assert bf.offset == 0
    assert bf.access == Access.RW
    assert bf.hardware == Hardware.NA
    assert bf.enum is None
    assert bf.metadata == {}


def test_hardware_exclusive_na() -> None:
    """Test that Hardware.NA must be exclusive in hardware flags."""
    with pytest.raises(ValueError, match="Hardware mode 'n' must be exclusive"):
        default_field(hardware=Hardware.NA | Hardware.INPUT)


def test_hardware_exclusive_queue() -> None:
    """Test that Hardware.QUEUE must be exclusive in hardware flags."""
    with pytest.raises(ValueError, match="Hardware mode 'q' must be exclusive"):
        default_field(hardware=Hardware.QUEUE | Hardware.INPUT)


def test_hardware_exclusive_fixed() -> None:
    """Test that Hardware.FIXED must be exclusive in hardware flags."""
    with pytest.raises(ValueError, match="Hardware mode 'f' must be exclusive"):
        default_field(hardware=Hardware.FIXED | Hardware.INPUT)


def test_hardware_queue_access() -> None:
    """Test that Hardware.QUEUE can only be used with certain access modes."""
    default_field(hardware=Hardware.QUEUE, access=Access.RW)
    default_field(hardware=Hardware.QUEUE, access=Access.RO)
    default_field(hardware=Hardware.QUEUE, access=Access.WO)

    with pytest.raises(ValueError, match="Hardware mode 'q' is allowed to use only with"):
        default_field(hardware=Hardware.QUEUE, access=Access.RW1C)


def test_hardware_enable_requires_input() -> None:
    """Test that Hardware.ENABLE requires Hardware.INPUT in hardware flags."""
    default_field(hardware=Hardware.ENABLE | Hardware.INPUT)

    with pytest.raises(ValueError, match="Hardware mode 'e' is allowed to use only with 'i'"):
        default_field(hardware=Hardware.ENABLE)


def test_reset_value_width() -> None:
    """Test that reset value width must not exceed field width."""
    with pytest.raises(ValueError, match="5 bits to represent, but field is 4 bits wide"):
        default_field(width=4, reset=0b10000)


def test_enum_values_width() -> None:
    """Test that enumeration member values must fit within field width."""
    enum = StrictEnum(
        name="enum",
        doc="",
        metadata={},
        members=(
            StrictEnumMember(
                name="ENUM_VALUE",
                doc="An enum value.",
                value=0b10000,  # requires 5 bits
                metadata={},
            ),
        ),
    )
    with pytest.raises(ValueError, match="5 bits to represent, but field is 4 bits wide"):
        default_field(width=4, enum=enum)


def test_enum_assigned_parent() -> None:
    """Test that field is assigned as parent to enum."""
    enum = StrictEnum(
        name="enum",
        doc="",
        metadata={},
        members=(
            StrictEnumMember(
                name="ENUM_VALUE",
                doc="An enum value.",
                value=1,
                metadata={},
            ),
        ),
    )
    field = default_field(enum=enum)

    assert field.enum
    assert field.enum.parent == field


def test_bit_indices() -> None:
    """Test bit_indices property."""
    bf = default_field(width=4, offset=2)
    assert list(bf.bit_indices) == [2, 3, 4, 5]


def test_byte_indices() -> None:
    """Test byte_indices property."""
    bf = default_field(width=16, offset=9)
    assert list(bf.byte_indices) == [1, 2, 3]


def test_lsb_msb() -> None:
    """Test lsb and msb properties."""
    bf = default_field(width=8, offset=4)
    assert bf.lsb == 4
    assert bf.msb == 11


def test_mask() -> None:
    """Test mask property."""
    bf = default_field(width=4, offset=4)
    expected_mask = (2**4 - 1) << 4
    assert bf.mask == expected_mask


def test_is_multibit() -> None:
    """Test is_multibit property."""
    assert not default_field(width=1).is_multibit
    assert default_field(width=2).is_multibit


def test_byte_select() -> None:
    """Test byte_select property."""
    bf = default_field(width=5, offset=13)
    assert bf.byte_select(1) == (15, 13)
    assert bf.byte_select(2) == (17, 16)
    with pytest.raises(ValueError, match="Provided byte_idx=0 has to be one of"):
        bf.byte_select(0)


def test_byte_select_self() -> None:
    """Test byte_select_self property."""
    bf = default_field(width=16, offset=7)
    assert bf.byte_select_self(0) == (0, 0)
    assert bf.byte_select_self(1) == (8, 1)
    assert bf.byte_select_self(2) == (15, 9)

    with pytest.raises(ValueError, match="Provided byte_idx=3 has to be one of"):
        bf.byte_select(3)
