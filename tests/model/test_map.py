"""Tests for a map."""

from __future__ import annotations

import pytest

from .utils import build_field, build_map, build_memory, build_register

# All tests below can be used in smoke testing
pytestmark = pytest.mark.smoke


def test_map_basic_properties() -> None:
    """Test basic map properties like size, granularity, and address calculations."""
    regmap = build_map(address_width=8, register_width=32, offset=0x10)

    assert regmap.size == 256  # 2^8
    assert regmap.granularity == 4  # 32 bits = 4 bytes
    assert regmap.address == 0x10  # root map address equals offset


def test_map_empty_items_validation() -> None:
    """Test that map validation fails when no items are provided."""
    with pytest.raises(ValueError, match="Empty map is not allowed"):
        build_map(items=())


def test_map_register_width_validation() -> None:
    """Test that map validation fails when register width is less than 8 bits."""
    with pytest.raises(ValueError, match=".*register_width.*"):
        build_map(register_width=4)


def test_map_unique_item_names() -> None:
    """Test that map validation fails when items have duplicate names."""
    reg1 = build_register(name="reg")
    reg2 = build_register(name="reg")

    with pytest.raises(ValueError, match="Some item names are not unique and used more than once"):
        build_map(items=(reg1, reg2))


def test_map_unique_item_offsets() -> None:
    """Test that map validation fails when items have duplicate offsets."""
    reg1 = build_register(name="reg1", offset=0)
    reg2 = build_register(name="reg2", offset=0)

    with pytest.raises(ValueError, match=".*offset.*unique.*"):
        build_map(items=(reg1, reg2))


def test_map_offset_alignment() -> None:
    """Test that map validation fails when item offsets are not aligned to map granularity."""
    # Create map with 32-bit registers (4-byte granularity)
    reg = build_register(offset=2)  # Unaligned offset

    with pytest.raises(ValueError, match=".*aligned.*"):
        build_map(items=(reg,), register_width=32)


def test_map_address_width_validation() -> None:
    """Test that map validation fails when items have address width greater than map."""
    submap = build_map(address_width=16)

    with pytest.raises(ValueError, match=".*address width.*"):
        build_map(items=(submap,), address_width=8)


def test_map_address_collisions() -> None:
    """Test that map validation fails when items have overlapping address ranges."""
    reg = build_register(offset=8)
    mem = build_memory(offset=0, address_width=8)  # Overlaps with reg

    with pytest.raises(ValueError, match=".*collision.*"):
        build_map(items=(reg, mem), register_width=32)


def test_map_register_fields_width() -> None:
    """Test that map validation fails when register fields exceed map register width."""
    field = build_field(offset=24, width=16)  # 24 + 16 = 40 bits
    reg = build_register(fields=(field,))

    with pytest.raises(ValueError, match=".*exceeds size.*"):
        build_map(items=(reg,), register_width=32)


def test_map_item_iteration() -> None:
    """Test map item iteration methods (maps, registers, memories)."""
    submap = build_map(name="submap", offset=0x100)
    reg = build_register(name="reg", offset=0x2000)
    mem = build_memory(name="mem", offset=0x3000)

    regmap = build_map(items=(submap, reg, mem), address_width=32)

    assert list(regmap.maps) == [submap]
    assert list(regmap.registers) == [reg]
    assert list(regmap.memories) == [mem]


def test_map_item_presence_checks() -> None:
    """Test map item presence check methods (has_maps, has_registers, has_memories)."""
    # Empty map with just a register
    map_regs = build_map()
    assert not map_regs.has_maps
    assert map_regs.has_registers
    assert not map_regs.has_memories

    # Map with submap
    submap = build_map(name="submap")
    map_with_submap = build_map(items=(submap,))
    assert map_with_submap.has_maps
    assert not map_with_submap.has_registers
    assert not map_with_submap.has_memories

    # Map with memory
    mem = build_memory(address_width=4)
    map_with_mem = build_map(items=(mem,))
    assert not map_with_mem.has_maps
    assert not map_with_mem.has_registers
    assert map_with_mem.has_memories


def test_map_root_detection() -> None:
    """Test that map correctly identifies itself as root or non-root."""
    root_map = build_map()
    assert root_map.is_root

    submap = build_map(name="submap")
    parent_map = build_map(items=(submap,))
    assert parent_map.is_root
    assert not submap.is_root


def test_map_parent_child_relationships() -> None:
    """Test that map correctly establishes parent-child relationships with items."""
    submap = build_map(name="submap", offset=0x100, address_width=8)
    reg = build_register(name="reg", offset=0x2000)
    mem = build_memory(name="mem", offset=0x3000)

    parent_map = build_map(items=(submap, reg, mem), address_width=32)

    assert submap.parent == parent_map
    assert reg.parent == parent_map
    assert mem.parent == parent_map


def test_map_address_space_boundaries() -> None:
    """Test that map validation fails when items exceed map address space."""
    reg = build_register(offset=0xFF0)  # Near the end of 8-bit address space

    with pytest.raises(ValueError, match=".*falling out.*"):
        build_map(items=(reg,), address_width=8)


def test_map_items_sorting() -> None:
    """Test that map items are correctly sorted by offset."""
    reg1 = build_register(name="reg1", offset=0x300)
    reg2 = build_register(name="reg2", offset=0x100)
    reg3 = build_register(name="reg3", offset=0x200)

    regmap = build_map(items=(reg1, reg2, reg3), address_width=32)

    # Items should be sorted by offset regardless of insertion order
    assert [item.name for item in regmap.items] == ["reg2", "reg3", "reg1"]
