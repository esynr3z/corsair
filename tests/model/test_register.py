"""Tests for a register."""

from __future__ import annotations

import pytest

import corsair as csr
from tests.model.utils import build_field, build_register

# All tests below can be used in smoke testing
pytestmark = pytest.mark.smoke


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
