"""Tests for a bitfield."""

from __future__ import annotations

import pytest

import corsair.model as csr

from .utils import build_enum, build_enum_member, build_field

# All tests below can be used in smoke testing
pytestmark = pytest.mark.smoke


def test_validation() -> None:
    """Test that a valid Field instance can be created."""
    bf = build_field()
    assert isinstance(bf, csr.Field)
    assert bf.name == "field_name"
    assert bf.doc == "A brief description.\n\nA detailed description of the field."
    assert bf.reset == 0
    assert bf.width == 8
    assert bf.offset == 0
    assert bf.access == csr.AccessMode.RW
    assert bf.hardware == csr.HardwareMode.NA
    assert bf.enum is None


def test_hardware_exclusive_na() -> None:
    """Test that HardwareMode.NA must be exclusive in hardware flags."""
    with pytest.raises(ValueError, match="Hardware mode 'n' must be exclusive"):
        build_field(hardware=csr.HardwareMode.NA | csr.HardwareMode.INPUT)


def test_hardware_exclusive_queue() -> None:
    """Test that HardwareMode.QUEUE must be exclusive in hardware flags."""
    with pytest.raises(ValueError, match="Hardware mode 'q' must be exclusive"):
        build_field(hardware=csr.HardwareMode.QUEUE | csr.HardwareMode.INPUT)


def test_hardware_exclusive_fixed() -> None:
    """Test that HardwareMode.FIXED must be exclusive in hardware flags."""
    with pytest.raises(ValueError, match="Hardware mode 'f' must be exclusive"):
        build_field(hardware=csr.HardwareMode.FIXED | csr.HardwareMode.INPUT)


def test_hardware_queue_access() -> None:
    """Test that HardwareMode.QUEUE can only be used with certain access modes."""
    build_field(hardware=csr.HardwareMode.QUEUE, access=csr.AccessMode.RW)
    build_field(hardware=csr.HardwareMode.QUEUE, access=csr.AccessMode.RO)
    build_field(hardware=csr.HardwareMode.QUEUE, access=csr.AccessMode.WO)

    with pytest.raises(ValueError, match="Hardware mode 'q' is allowed to use only with"):
        build_field(hardware=csr.HardwareMode.QUEUE, access=csr.AccessMode.RW1C)


def test_hardware_enable_requires_input() -> None:
    """Test that HardwareMode.ENABLE requires HardwareMode.INPUT in hardware flags."""
    build_field(hardware=csr.HardwareMode.ENABLE | csr.HardwareMode.INPUT)

    with pytest.raises(ValueError, match="Hardware mode 'e' is allowed to use only with 'i'"):
        build_field(hardware=csr.HardwareMode.ENABLE)


def test_reset_value_width() -> None:
    """Test that reset value width must not exceed field width."""
    with pytest.raises(ValueError, match="5 bits to represent, but field is 4 bits wide"):
        build_field(width=4, reset=0b10000)


def test_enum_values_width() -> None:
    """Test that enumeration member values must fit within field width."""
    enum = build_enum(
        members=(build_enum_member(name="ENUM_VALUE", value=0b10000),),
    )
    with pytest.raises(ValueError, match="5 bits to represent, but field is 4 bits wide"):
        build_field(width=4, enum=enum)


def test_enum_assigned_parent() -> None:
    """Test that field is assigned as parent to enum."""
    enum = build_enum(
        members=(build_enum_member(),),
    )
    field = build_field(enum=enum)

    assert field.enum
    assert field.enum.parent == field


def test_bit_indices() -> None:
    """Test bit_indices property."""
    bf = build_field(width=4, offset=2)
    assert list(bf.bit_indices) == [2, 3, 4, 5]


def test_byte_indices() -> None:
    """Test byte_indices property."""
    bf = build_field(width=16, offset=9)
    assert list(bf.byte_indices) == [1, 2, 3]


def test_lsb_msb() -> None:
    """Test lsb and msb properties."""
    bf = build_field(width=8, offset=4)
    assert bf.lsb == 4
    assert bf.msb == 11


def test_mask() -> None:
    """Test mask property."""
    bf = build_field(width=4, offset=4)
    expected_mask = (2**4 - 1) << 4
    assert bf.mask == expected_mask


def test_is_multibit() -> None:
    """Test is_multibit property."""
    assert not build_field(width=1).is_multibit
    assert build_field(width=2).is_multibit


def test_byte_select() -> None:
    """Test byte_select property."""
    bf = build_field(width=5, offset=13)
    assert bf.byte_select(1) == (15, 13)
    assert bf.byte_select(2) == (17, 16)
    with pytest.raises(ValueError, match="Provided byte_idx=0 has to be one of"):
        bf.byte_select(0)


def test_byte_select_self() -> None:
    """Test byte_select_self property."""
    bf = build_field(width=16, offset=7)
    assert bf.byte_select_self(0) == (0, 0)
    assert bf.byte_select_self(1) == (8, 1)
    assert bf.byte_select_self(2) == (15, 9)

    with pytest.raises(ValueError, match="Provided byte_idx=3 has to be one of"):
        bf.byte_select(3)
