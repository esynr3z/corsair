#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Register module tests
"""

import pytest
from corsair import Register, BitField
import copy


def test_create():
    """Test of a register creation."""
    # create with defaults
    reg = Register()
    with pytest.raises(AssertionError):
        # address is None by default
        reg.validate()

    # create with non-default values
    name = 'REGA'
    description = 'Register A'
    address = 0x4
    bitfields = [
        BitField('BFA', 'Bit field A', lsb=0),
        BitField('BFB', 'Bit field B', lsb=1),
        BitField('BFC', 'Bit field C', lsb=2)
    ]
    reg = Register(name, description, address)
    reg.add_bitfields(bitfields)
    print(repr(reg))
    print(reg)
    assert ((name, description, address, bitfields) ==
            (reg.name, reg.description, reg.address, reg.bitfields))


def test_eq():
    """Test of (non)equality comparision of registes."""
    reg1 = Register('reg_a')
    reg1.add_bitfields([
        BitField('bf_a', 'Bit field A', lsb=0),
        BitField('bf_b', 'Bit field B', lsb=1)
    ])
    reg2 = copy.deepcopy(reg1)
    assert reg1 == reg2
    reg2['bf_a'].access = 'wo'
    assert reg1 != reg2


def test_name():
    """Name property"""
    # init
    reg = Register(name='abc', address=0)
    assert reg.name == 'abc'
    # set
    reg.name = 'cde'
    assert reg.name == 'cde'
    # set wrong
    with pytest.raises(ValueError):
        reg.name = 5
    reg.name = '5cde'
    with pytest.raises(AssertionError):
        reg.validate()


def test_description():
    """Description property"""
    # init
    reg = Register(description='abc', address=0)
    assert reg.description == 'abc'
    # set
    reg.description = 'cde'
    assert reg.description == 'cde'
    # set wrong
    with pytest.raises(ValueError):
        reg.description = 5


def test_address():
    """Address property"""
    # init
    reg = Register(address=0x5)
    assert reg.address == 0x5
    reg = Register(address='0x5')
    assert reg.address == 0x5
    # set
    reg.address = 0x3
    assert reg.address == 0x3
    reg.address = '0x6'
    assert reg.address == 0x6
    # set wrong
    with pytest.raises(ValueError):
        reg.address = 'zz'
    reg.address = None
    with pytest.raises(AssertionError):
        reg.validate()


def test_add_bitfields():
    """Test of adding field to a register."""
    # single
    reg = Register('REGA', 'Register A')
    bf = BitField('bf_a', 'Bit field A')
    reg.add_bitfields(bf)
    assert bf == reg['bf_a']
    assert bf == reg[0]
    # multiple
    reg = Register('REGA', 'Register A')
    bf = [
        BitField('bf_a', 'Bit field A', lsb=0),
        BitField('bf_b', 'Bit field B', lsb=1)
    ]
    reg.add_bitfields(bf)
    assert bf[0] == reg['bf_a']
    assert bf[0] == reg[0]
    assert bf[1] == reg['bf_b']
    assert bf[1] == reg[1]


def test_access_bitfields():
    """Test of trying to get bit field with wrong name/index."""
    reg = Register('REGA', 'Register A')
    bf = [
        BitField('bf_a', 'Bit field A', lsb=0),
        BitField('bf_b', 'Bit field B', lsb=1)
    ]
    reg.add_bitfields(bf)
    with pytest.raises(KeyError):
        reg['bf_c']
    with pytest.raises(KeyError):
        reg[3]


def test_field_name_conflict():
    """Test of adding a field with a name that already present in a register."""
    reg = Register('REGA', 'Register A')
    reg.add_bitfields(BitField('bf_a', 'Bit field A', lsb=0))
    with pytest.raises(AssertionError):
        reg.add_bitfields(BitField('bf_a', 'Bit field A', lsb=0))


def test_field_position_conflict():
    """Test of adding a field with position that  overlaps with other field in a register."""
    reg = Register('REGA', 'Register A')
    reg.add_bitfields(BitField('bf_a', 'Bit field A', lsb=0, width=8))
    reg.add_bitfields(BitField('bf_b', 'Bit field B', lsb=8, width=8))
    with pytest.raises(AssertionError):
        reg.add_bitfields(BitField('bf_c', 'Bit field C', lsb=4, width=10))


def test_field_order():
    """Test of adding fields and check that they are presented in ascending order in a register."""
    reg = Register('REGA', 'Register A')
    reg.add_bitfields(BitField('bf_a', 'Bit field A', lsb=0, width=3))
    reg.add_bitfields(BitField('bf_b', 'Bit field B', lsb=16, width=1))
    reg.add_bitfields(BitField('bf_c', 'Bit field C', lsb=5, width=6))
    reg.add_bitfields(BitField('bf_d', 'Bit field D', lsb=18, width=12))
    assert reg.bitfield_names == ['bf_a', 'bf_c', 'bf_b', 'bf_d']


def test_field_datawidth_conflict():
    """Wait exception when bf.msb value exceeds data width."""
    reg = Register('reg_a', 'Register A', 0x4)
    with pytest.raises(AssertionError):
        reg.add_bitfields([
            BitField('bf_a', 'Bit field A', lsb=0, width=35),
        ])


def test_bitfields_unique():
    """All bitfields must have unique names"""
    # name
    reg = Register('reg_a', 'Register A')
    reg.add_bitfields(BitField('bf_a', 'Bit field A', lsb=0, width=3))
    reg.add_bitfields(BitField('bf_b', 'Bit field B', lsb=16, width=1))
    reg[1].name = 'bf_a'
    with pytest.raises(AssertionError):
        reg.validate()


def test_custom_props():
    """Add custom properties on creation"""
    # init
    reg = Register()
    assert reg.etc == {}
    reg = Register(the_answer=42)
    assert reg.etc['the_answer'] == 42
    assert reg.as_dict()['the_answer'] == 42
