#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Register map module tests
"""

import pytest
from corsair import config, Register, BitField, RegisterMap
import copy


def test_create():
    """Test of a register map creation."""
    name = 'reg_a'
    description = 'Register A'
    address = 0x4
    reg = Register(name, description, address)
    reg.add_bitfields([
        BitField('bf_a', 'Bit field A', lsb=0),
        BitField('bf_b', 'Bit field B', lsb=1)
    ])
    rmap = RegisterMap()
    rmap.add_registers(reg)
    print(repr(rmap))
    print(rmap)
    assert rmap['reg_a'] == reg


def test_eq():
    """Test of equality comparision of register maps."""
    reg = Register('reg_a', 'Register A', 0x4)
    reg.add_bitfields([
        BitField('bf_a', 'Bit field A', lsb=0),
        BitField('bf_b', 'Bit field B', lsb=1)
    ])
    rmap1 = RegisterMap()
    rmap1.add_registers(reg)
    rmap2 = copy.deepcopy(rmap1)
    assert rmap1 == rmap2


def test_ne():
    """Test of non equality comparision of register maps."""
    reg = Register('reg_a', 'Register A', 0x4)
    reg.add_bitfields([
        BitField('bf_a', 'Bit field A', lsb=0),
        BitField('bf_b', 'Bit field B', lsb=1)
    ])
    rmap1 = RegisterMap()
    rmap1.add_registers(reg)
    rmap2 = copy.deepcopy(rmap1)
    rmap2['reg_a']['bf_b'].reset = 1
    assert rmap1 != rmap2


def test_add_registers():
    """Test of adding several registers to a map"""
    reg_a = Register('reg_a', 'Register A', 0x8)
    reg_b = Register('reg_b', 'Register B', 0xC)
    rmap = RegisterMap()
    rmap.add_registers([reg_a, reg_b])
    assert rmap[0] == reg_a
    assert rmap['reg_a'] == reg_a
    assert rmap[1] == reg_b
    assert rmap['reg_b'] == reg_b


def test_reg_name_conflict():
    """Test of adding register with a name that already present in a map."""
    rmap = RegisterMap()
    rmap.add_registers(Register('reg_a', 'Register A', 0x8))
    with pytest.raises(AssertionError):
        rmap.add_registers(Register('reg_a', 'Register A copypaste', 0x8))


def test_reg_no_addr_first():
    """Test of adding first register with no address to a map"""
    rmap = RegisterMap()
    with pytest.raises(AssertionError):
        rmap.add_registers(Register('reg_a', 'Register A'))


def test_reg_no_addr_no_incr():
    """Test of adding register with no address to a map when address auto increment is deisabled."""
    rmap = RegisterMap()
    rmap.add_registers(Register('reg_a', 'Register A', 0x0))
    with pytest.raises(AssertionError):
        rmap.add_registers(Register('reg_b', 'Register B'))


def test_reg_addr_align_data_width():
    """Test of adding register with address not aligned to a proper value (based on a data width)."""
    globcfg = config.default_globcfg()
    globcfg['address_alignment'] = 'data_width'
    globcfg['data_width'] = 32
    config.set_globcfg(globcfg)
    rmap = RegisterMap()
    with pytest.raises(AssertionError):
        rmap.add_registers(Register('reg_a', 'Register A', 0x2))
    config.set_globcfg(config.default_globcfg())


def test_reg_addr_align_custom():
    """Test of adding register with address not aligned to a proper value (based on a custom value)."""
    globcfg = config.default_globcfg()
    globcfg['address_alignment'] = 128
    config.set_globcfg(globcfg)
    rmap = RegisterMap()
    with pytest.raises(AssertionError):
        rmap.add_registers(Register('reg_a', 'Register A', 0x4))
    config.set_globcfg(config.default_globcfg())


def test_reg_addr_align_none():
    """Test of adding register with address not aligned to a proper value (based on a custom value)."""
    globcfg = config.default_globcfg()
    globcfg['address_alignment'] = 'none'
    globcfg['data_width'] = 32
    config.set_globcfg(globcfg)
    rmap = RegisterMap()
    # no exception
    rmap.add_registers(Register('reg_a', 'Register A', 0x2))
    config.set_globcfg(config.default_globcfg())


def test_reg_addr_conflict():
    """Test of adding register with an address that already present in a map."""
    rmap = RegisterMap()
    rmap.add_registers(Register('reg_a', 'Register A', 0x0))
    with pytest.raises(AssertionError):
        rmap.add_registers(Register('reg_b', 'Register B', 0x0))


def test_reg_addr_order():
    """Test of adding registers and check that they are presented in ascending order in a map."""
    rmap = RegisterMap()
    rmap.add_registers(Register('reg_a', 'Register A', 0x0))
    rmap.add_registers(Register('reg_b', 'Register B', 0x10))
    rmap.add_registers(Register('reg_c', 'Register C', 0x4))
    rmap.add_registers(Register('reg_d', 'Register D', 0x14))
    assert rmap.reg_names == ['reg_a', 'reg_c', 'reg_b', 'reg_d']


def test_reg_addr_auto_incr_data_width():
    """Test of auto increment of a register's address based on interface data width."""
    globcfg = config.default_globcfg()
    globcfg['address_increment'] = 'data_width'
    globcfg['data_width'] = 64
    config.set_globcfg(globcfg)
    rmap = RegisterMap()
    rmap.add_registers(Register('reg_a', 'Register A', 0x0))
    rmap.add_registers(Register('reg_b', 'Register B'))
    assert rmap['reg_b'].address == 0x8
    config.set_globcfg(config.default_globcfg())


def test_reg_addr_auto_incr_custom():
    """Test of auto increment of a register's address."""
    globcfg = config.default_globcfg()
    globcfg['address_alignment'] = 'none'
    globcfg['address_increment'] = 0x2
    config.set_globcfg(globcfg)
    rmap = RegisterMap()
    rmap.add_registers(Register('reg_a', 'Register A', 0x0))
    rmap.add_registers(Register('reg_b', 'Register B'))
    assert rmap['reg_b'].address == 0x2
    config.set_globcfg(config.default_globcfg())


def test_reg_addr_auto_incr_align():
    """Test of alignment check of an auto incremented register's address."""
    globcfg = config.default_globcfg()
    globcfg['address_alignment'] = 0x4
    globcfg['address_increment'] = 0x2
    config.set_globcfg(globcfg)
    rmap = RegisterMap()
    rmap.add_registers(Register('reg_a', 'Register A', 0x0))
    with pytest.raises(AssertionError):
        rmap.add_registers(Register('reg_b', 'Register B'))
    config.set_globcfg(config.default_globcfg())


def test_reg_unique():
    """All registers must have unique names"""
    rmap = RegisterMap()
    rmap.add_registers([
        Register('rega', 'Register A', 0x0),
        Register('regb', 'Register B', 0x4),
    ])
    rmap[1].name = 'rega'
    with pytest.raises(AssertionError):
        rmap.validate()
