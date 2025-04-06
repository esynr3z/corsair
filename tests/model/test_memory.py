"""Tests for a memory block."""

from __future__ import annotations

import pytest

import corsair as csr
from tests.model.utils import build_memory

# All tests below can be used in smoke testing
pytestmark = pytest.mark.smoke


def test_memory_capacity_calculation() -> None:
    """Test that memory capacity is correctly calculated as 2^address_width."""
    memory = build_memory(address_width=12)
    assert memory.capacity == 2**12

    memory = build_memory(address_width=8)
    assert memory.capacity == 2**8


def test_memory_size_calculation() -> None:
    """Test that memory size is correctly calculated as capacity * granularity."""
    memory = build_memory(address_width=12, data_width=32)
    assert memory.size == 2**12 * 4

    memory = build_memory(address_width=8, data_width=16)
    assert memory.size == 2**8 * 2


def test_memory_granularity_calculation() -> None:
    """Test that memory granularity is correctly calculated as ceil(data_width/8)."""
    memory = build_memory(data_width=32)
    assert memory.granularity == 4

    memory = build_memory(data_width=12)
    assert memory.granularity == 2


def test_memory_access_matches_style() -> None:
    """Test that memory access property correctly reflects the style's access category."""
    memory = build_memory(style=csr.MemoryStyle.INTERNAL_RO)
    assert memory.access == csr.AccessCategory.RO

    memory = build_memory(style=csr.MemoryStyle.INTERNAL_WO)
    assert memory.access == csr.AccessCategory.WO

    memory = build_memory(style=csr.MemoryStyle.INTERNAL_RW)
    assert memory.access == csr.AccessCategory.RW


def test_memory_with_valid_initial_values() -> None:
    """Test memory creation with valid initial values."""
    initial_values = (
        (0, 0xFFFFFFFF),
        (4, 0x12345678),
        (8, 0x00000000),
    )
    memory = build_memory(initial_values=initial_values)
    assert memory.initial_values == initial_values


def test_memory_with_invalid_initial_values() -> None:
    """Test that memory creation fails with invalid initial values."""
    # Test with address beyond memory size (2^address_width)
    with pytest.raises(ValueError, match="initial value 0 address 0x100 is out of memory capacity"):
        build_memory(address_width=8, initial_values=((256, 0),))  # 256 >= 2^8

    # Test with value beyond memory data width (2^data_width)
    with pytest.raises(ValueError, match="initial value 0 data 0x10000 is out of memory data width"):
        build_memory(data_width=16, initial_values=((0, 0x10000),))  # 0x10000 >= 2^16

    # Test with invalid value (negative)
    with pytest.raises(ValueError, match="Input should be greater than or equal to 0"):
        build_memory(initial_values=((0, -1),))

    # Test with invalid value (negative)
    with pytest.raises(ValueError, match="Input should be greater than or equal to 0"):
        build_memory(initial_values=((-1, 0),))


def test_memory_with_minimum_valid_widths() -> None:
    """Test memory creation with minimum valid address and data widths."""
    memory = build_memory(address_width=1, data_width=1)
    assert memory.address_width == 1
    assert memory.data_width == 1


def test_memory_with_invalid_address_width() -> None:
    """Test that memory creation fails with invalid address width."""
    with pytest.raises(ValueError, match="Input should be greater than 0"):
        build_memory(address_width=0)

    with pytest.raises(ValueError, match="Input should be greater than 0"):
        build_memory(address_width=-1)


def test_memory_with_invalid_data_width() -> None:
    """Test that memory creation fails with invalid data width."""
    with pytest.raises(ValueError, match="Input should be greater than 0"):
        build_memory(data_width=0)

    with pytest.raises(ValueError, match="Input should be greater than 0"):
        build_memory(data_width=-1)


def test_memory_with_internal_ro_style() -> None:
    """Test memory creation with INTERNAL_RO style."""
    memory = build_memory(style=csr.MemoryStyle.INTERNAL_RO)
    assert memory.style == csr.MemoryStyle.INTERNAL_RO
    assert memory.style.is_ro


def test_memory_with_internal_wo_style() -> None:
    """Test memory creation with INTERNAL_WO style."""
    memory = build_memory(style=csr.MemoryStyle.INTERNAL_WO)
    assert memory.style == csr.MemoryStyle.INTERNAL_WO
    assert memory.style.is_wo


def test_memory_with_internal_rw_style() -> None:
    """Test memory creation with INTERNAL_RW style."""
    memory = build_memory(style=csr.MemoryStyle.INTERNAL_RW)
    assert memory.style == csr.MemoryStyle.INTERNAL_RW
    assert memory.style.is_rw


def test_memory_with_external_ro_style() -> None:
    """Test memory creation with EXTERNAL_RO style."""
    memory = build_memory(style=csr.MemoryStyle.EXTERNAL_RO)
    assert memory.style == csr.MemoryStyle.EXTERNAL_RO
    assert memory.style.is_ro


def test_memory_with_external_wo_style() -> None:
    """Test memory creation with EXTERNAL_WO style."""
    memory = build_memory(style=csr.MemoryStyle.EXTERNAL_WO)
    assert memory.style == csr.MemoryStyle.EXTERNAL_WO
    assert memory.style.is_wo


def test_memory_with_external_rw_style() -> None:
    """Test memory creation with EXTERNAL_RW style."""
    memory = build_memory(style=csr.MemoryStyle.EXTERNAL_RW)
    assert memory.style == csr.MemoryStyle.EXTERNAL_RW
    assert memory.style.is_rw


def test_memory_with_valid_metadata() -> None:
    """Test memory creation with valid metadata."""
    memory = build_memory(metadata={"custom_field": "test_value"})
    assert memory.metadata.custom_field == "test_value"  # type: ignore reportAttributeAccessIssue
