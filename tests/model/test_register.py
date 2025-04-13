"""Tests for a register."""

from __future__ import annotations

import pytest

import corsair as csr
from tests.model.utils import build_field, build_register


def test_validation() -> None:
    """Test that a valid Register instance can be created."""
    reg = build_register()
    assert reg.name == "test_register"
    assert reg.doc == "Test register."
    assert reg.offset == 0
    assert reg.fields[0].name == "field_name"
    assert reg.fields[0].offset == 0
    assert reg.fields[0].access == csr.AccessMode.RW


def test_register_width() -> None:
    """Test that register width is correctly derived from fields."""
    reg = build_register(
        fields=(
            build_field(name="field1", offset=0, width=16),
            build_field(name="field2", offset=32, width=16),
        )
    )
    assert reg.width == 48


def test_register_access_category() -> None:
    """Test that register access category is correctly determined from fields."""
    # All read-only field.
    ro_field = build_field(name="ro_field", offset=0, width=16, access=csr.AccessMode.RO)
    rolh_field = build_field(name="rolh_field", offset=16, width=16, access=csr.AccessMode.ROLH)
    reg_ro = build_register(fields=(ro_field, rolh_field))
    assert reg_ro.access == csr.AccessCategory.RO

    # All write-only fields.
    wo_field = build_field(name="wo_field", offset=0, width=16, access=csr.AccessMode.WO)
    wosc_field = build_field(name="wosc_field", offset=16, width=1, access=csr.AccessMode.WOSC)
    reg_wo = build_register(fields=(wo_field, wosc_field))
    assert reg_wo.access == csr.AccessCategory.WO

    # Mixed access fields.
    ro_field = build_field(name="ro_field", offset=0, width=16, access=csr.AccessMode.RO)
    rw_field = build_field(name="rw_field", offset=16, width=16, access=csr.AccessMode.RW)
    reg_rw = build_register(fields=(ro_field, rw_field))
    assert reg_rw.access == csr.AccessCategory.RW


def test_register_reset_value() -> None:
    """Test that register reset value is correctly calculated from fields."""
    field1 = build_field(name="field1", offset=0, width=8, reset=5)
    field2 = build_field(name="field2", offset=8, width=8, reset=3)
    reg = build_register(fields=(field1, field2))
    expected_reset = (5 << 0) | (3 << 8)
    assert reg.reset == expected_reset


def test_register_reset_binstr() -> None:
    """Test binary string representation of reset value with unknown bits."""
    # Field1 has a non-zero reset; Field2 has unknown reset (translated to unknown bits 'x').
    field1 = build_field(name="field1", offset=0, width=8, reset=5)  # "00000101"
    field2 = build_field(name="field2", offset=8, width=8, reset=None)  # becomes "xxxxxxxx"
    reg = build_register(fields=(field1, field2))
    # Expected: positions [0:8] -> "00000101", [8:16] -> "xxxxxxxx"
    # Then the full bits list is reversed.
    expected_bin_part = "".join(reversed(list("00000101")))
    expected_binstr = "x" * 8 + expected_bin_part
    assert reg.reset_binstr == expected_binstr


def test_register_reset_hexstr() -> None:
    """Test hexadecimal string representation of reset value with unknown nibbles."""
    # Using one field that covers the entire register width with known reset.
    field_full = build_field(name="field_full", offset=0, width=16, reset=0x2BCA)
    reg = build_register(fields=(field_full,))
    assert reg.reset_hexstr == "2bca"


def test_fields_sorting() -> None:
    """Test that fields are sorted by LSB position."""
    field_a = build_field(name="field_a", offset=8, width=8, reset=1)
    field_b = build_field(name="field_b", offset=0, width=8, reset=2)
    reg = build_register(fields=(field_a, field_b))
    # After sorting, the field with offset 0 should come first.
    assert reg.fields[0].offset == 0
    assert reg.fields[1].offset == 8


def test_fields_unique_names() -> None:
    """Test that field names within register are unique."""
    field_dup1 = build_field(name="dup", offset=0, width=8)
    field_dup2 = build_field(name="dup", offset=8, width=8)
    with pytest.raises(ValueError, match="some field names are not unique"):
        build_register(fields=(field_dup1, field_dup2))


def test_fields_no_overlap() -> None:
    """Test that fields don't overlap in their bit positions."""
    # Overlapping fields: field1 covers bits 0..7, field2 covers bits 4..11.
    field1 = build_field(name="field1", offset=0, width=8, reset=1)
    field2 = build_field(name="field2", offset=4, width=8, reset=2)
    with pytest.raises(ValueError, match="overlaps with other fields"):
        build_register(fields=(field1, field2))


def test_register_fields_with_reserved_full_width() -> None:
    """Test case: field spans the entire register width (no reserved fields)."""
    field_full = build_field(name="full_field", offset=0, width=32)
    reg_full = build_register(name="reg_full", fields=(field_full,))
    _ = csr.Map(
        name="test_map",
        doc="Test map",
        offset=0,
        address_width=16,
        register_width=32,
        items=(reg_full,),
    )
    reserved_fields = reg_full.fields_with_reserved
    assert len(reserved_fields) == 1
    assert reserved_fields[0].name == "full_field"


def test_register_fields_with_reserved_lsb() -> None:
    """Test case: field at LSB, reserved bits at MSB."""
    field_lsb = build_field(name="lsb_field", offset=0, width=8)
    reg_lsb = build_register(name="reg_lsb", fields=(field_lsb,))
    _ = csr.Map(
        name="test_map",
        doc="Test map",
        offset=0,
        address_width=16,
        register_width=32,
        items=(reg_lsb,),
    )
    reserved_fields = reg_lsb.fields_with_reserved
    assert len(reserved_fields) == 2
    assert reserved_fields[0].name == "lsb_field"
    assert reserved_fields[1].name == "_reserved_31_8"
    assert reserved_fields[1].offset == 8
    assert reserved_fields[1].width == 24
    assert reserved_fields[1].access == csr.AccessMode.RO
    assert reserved_fields[1].hardware == csr.HardwareMode.NA


def test_register_fields_with_reserved_msb() -> None:
    """Test case: reserved bits at LSB, field at MSB."""
    field_msb = build_field(name="msb_field", offset=24, width=8)
    reg_msb = build_register(name="reg_msb", fields=(field_msb,))
    _ = csr.Map(
        name="test_map",
        doc="Test map",
        offset=0,
        address_width=16,
        register_width=32,
        items=(reg_msb,),
    )
    reserved_fields = reg_msb.fields_with_reserved
    assert len(reserved_fields) == 2
    assert reserved_fields[0].name == "_reserved_23_0"
    assert reserved_fields[0].offset == 0
    assert reserved_fields[0].width == 24
    assert reserved_fields[1].name == "msb_field"


def test_register_fields_with_reserved_middle() -> None:
    """Test case: two fields in the middle, creating three reserved sections."""
    field1 = build_field(name="field1", offset=8, width=8)
    field2 = build_field(name="field2", offset=20, width=4)
    reg_mid = build_register(name="reg_mid", fields=(field1, field2))
    _ = csr.Map(
        name="test_map",
        doc="Test map",
        offset=0,
        address_width=16,
        register_width=32,
        items=(reg_mid,),
    )

    reserved_fields = reg_mid.fields_with_reserved
    assert len(reserved_fields) == 5
    assert reserved_fields[0].name == "_reserved_7_0"
    assert reserved_fields[0].offset == 0
    assert reserved_fields[0].width == 8
    assert reserved_fields[1].name == "field1"
    assert reserved_fields[2].name == "_reserved_19_16"
    assert reserved_fields[2].offset == 16
    assert reserved_fields[2].width == 4
    assert reserved_fields[3].name == "field2"
    assert reserved_fields[4].name == "_reserved_31_24"
    assert reserved_fields[4].offset == 24
    assert reserved_fields[4].width == 8


# TODO: Add tests for register arrays
# TODO: Add tests for hardware signals generation
# TODO: Add tests for complex access modes interactions
