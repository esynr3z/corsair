#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Bit field module tests
"""

from corsair.enum import EnumValue
import pytest
from corsair import BitField
import copy


def test_create():
    """Test of a bit field creation."""
    # create with defaults
    bf = BitField()
    bf.validate()

    # create with non-default values
    name = 'ABC'
    description = 'abc'
    reset = 1
    width = 6
    lsb = 0
    access = 'ro'
    hardware = 'i'
    bf = BitField(name=name, description=description, reset=reset, width=width,
                  lsb=lsb, access=access, hardware=hardware)
    print(repr(bf))
    print(bf)
    assert ((name, description, reset, width, lsb, access, hardware) ==
            (bf.name, bf.description, bf.reset, bf.width, bf.lsb, bf.access, bf.hardware))


def test_eq():
    """Test of (non)equality comparision of bit fields."""
    bf1 = BitField('bf_a', reset=2)
    bf2 = copy.deepcopy(bf1)
    assert bf1 == bf2
    bf2.reset = 3
    assert bf1 != bf2


def test_name():
    """Name property"""
    # init
    bf = BitField(name='abc')
    assert bf.name == 'abc'
    # set
    bf.name = 'cde'
    assert bf.name == 'cde'
    # set wrong
    with pytest.raises(ValueError):
        bf.name = 5
    bf.name = '5cde'
    with pytest.raises(AssertionError):
        bf.validate()


def test_description():
    """Description property"""
    # init
    bf = BitField(description='abc')
    assert bf.description == 'abc'
    # set
    bf.description = 'cde'
    assert bf.description == 'cde'
    # set wrong
    with pytest.raises(ValueError):
        bf.description = 5


def test_reset():
    """Reset property"""
    # init
    bf = BitField(reset=0x5)
    assert bf.reset == 0x5
    bf = BitField(reset='0x5')
    assert bf.reset == 0x5
    # set
    bf.reset = 0x3
    assert bf.reset == 0x3
    bf.reset = '0x6'
    assert bf.reset == 0x6
    # set wrong
    with pytest.raises(ValueError):
        bf.reset = 'zz'


def test_lsb():
    """LCB property"""
    # init
    bf = BitField(lsb=0x5)
    assert bf.lsb == 0x5
    bf = BitField(lsb='0x5')
    assert bf.lsb == 0x5
    # set
    bf.lsb = 0x3
    assert bf.lsb == 0x3
    bf.lsb = '0x6'
    assert bf.lsb == 0x6
    # set wrong
    with pytest.raises(ValueError):
        bf.lsb = 'zz'


def test_width():
    """Width property"""
    # init
    bf = BitField(width=0x5)
    assert bf.width == 0x5
    bf = BitField(width='0x5')
    assert bf.width == 0x5
    # set
    bf.width = 0x3
    assert bf.width == 0x3
    bf.width = '0x6'
    assert bf.width == 0x6
    # set wrong
    with pytest.raises(ValueError):
        bf.width = 'zz'


def test_msb():
    """MSB property"""
    bf = BitField('bf_a', lsb=2, width=4)
    assert bf.msb == 5


def test_access():
    """Access property"""
    # init
    bf = BitField(access='ro')
    assert bf.access == 'ro'
    # set
    bf.access = 'rw'
    assert bf.access == 'rw'
    # set wrong
    with pytest.raises(ValueError):
        bf.access = 5
    bf.access = 'w0'
    with pytest.raises(AssertionError):
        bf.validate()


def test_hardware():
    """Hardware property"""
    # init
    bf = BitField(hardware='ioq')
    assert bf.hardware == 'ioq'
    # set
    bf.hardware = 'iol'
    assert bf.hardware == 'iol'
    # set wrong
    with pytest.raises(ValueError):
        bf.hardware = 'rw'
    bf.access = 'rw'
    bf.hardware = 'iq'
    with pytest.raises(AssertionError):
        bf.validate()


def test_bits():
    """Test of adding a field with position that  overlaps with other field in a register."""
    bf = BitField('bf_a', lsb=5, width=4)
    assert bf.bits == [5, 6, 7, 8]


def test_byte_strobes():
    """Test byte strobes info of the bit field."""
    bf_a = BitField('bf_a', lsb=0, width=16)
    bf_b = BitField('bf_b', lsb=0, width=13)
    bf_c = BitField('bf_c', lsb=8, width=16)
    bf_d = BitField('bf_d', lsb=14, width=14)
    assert bf_a.byte_strobes == {0: {'bf_lsb': 0, 'bf_msb': 7,
                                     'wdata_lsb': 0, 'wdata_msb': 7},
                                 1: {'bf_lsb': 8, 'bf_msb': 15,
                                     'wdata_lsb': 8, 'wdata_msb': 15}}
    assert bf_b.byte_strobes == {0: {'bf_lsb': 0, 'bf_msb': 7,
                                     'wdata_lsb': 0, 'wdata_msb': 7},
                                 1: {'bf_lsb': 8, 'bf_msb': 12,
                                     'wdata_lsb': 8, 'wdata_msb': 12}}
    assert bf_c.byte_strobes == {1: {'bf_lsb': 0, 'bf_msb': 7,
                                     'wdata_lsb': 8, 'wdata_msb': 15},
                                 2: {'bf_lsb': 8, 'bf_msb': 15,
                                     'wdata_lsb': 16, 'wdata_msb': 23}}
    assert bf_d.byte_strobes == {1: {'bf_lsb': 0, 'bf_msb': 1,
                                     'wdata_lsb': 14, 'wdata_msb': 15},
                                 2: {'bf_lsb': 2, 'bf_msb': 9,
                                     'wdata_lsb': 16, 'wdata_msb': 23},
                                 3: {'bf_lsb': 10, 'bf_msb': 13,
                                     'wdata_lsb': 24, 'wdata_msb': 27}}


def test_add_enum():
    """Test of adding enum to a bitfield"""
    # single
    bf = BitField('bf_a', 'Bit field A')
    enum = EnumValue("enum_a", 1, "descr")
    bf.add_enums(enum)
    assert enum == bf['enum_a']
    assert enum == bf[0]
    # multiple
    bf = BitField('bf_a', 'Bit field A')
    enums = [
        EnumValue('enum_a', 0, 'Enum A'),
        EnumValue('enum_b', 1, 'Enum B')
    ]
    bf.add_enums(enums)
    assert enums[0] == bf['enum_a']
    assert enums[0] == bf[0]
    assert enums[1] == bf['enum_b']
    assert enums[1] == bf[1]
    # wrong access
    with pytest.raises(KeyError):
        bf['enum_c']
    with pytest.raises(KeyError):
        bf[2]


def test_enum_name_conflict():
    """Test of adding an enum  with a name that already present in a bitfield"""
    bf = BitField('bf_a', 'Bit field A')
    bf.add_enums(EnumValue('enum_a', 0, 'Enum A'))
    with pytest.raises(AssertionError):
        bf.add_enums(EnumValue('enum_a', 1, 'Enum B',))


def test_enum_value_conflict():
    """Test of adding an enum with a value that already present in a bitfield"""
    bf = BitField('bf_a', 'Bit field A')
    bf.add_enums(EnumValue('enum_a', 0, 'Enum A'))
    with pytest.raises(AssertionError):
        bf.add_enums(EnumValue('enum_b', 0, 'Enum B'))


def test_enum_order():
    """Test of adding enums and check that they are presented in ascending order in a bitfield."""
    bf = BitField('bf_a', 'Bit field A', width=8)
    bf.add_enums(EnumValue('enum_a', 3, 'Enum A'))
    bf.add_enums(EnumValue('enum_b', 0, 'Enum B'))
    bf.add_enums(EnumValue('enum_c', 5, 'Enum C'))
    bf.add_enums(EnumValue('enum_d', 1, 'Enum D'))
    assert bf.enum_names == ['enum_b', 'enum_d', 'enum_a', 'enum_c']


def test_enum_width_conflict():
    """Wait exception when enum value bit length exce exceeds bitfield width."""
    bf = BitField('bf_a', 'Bit field A', width=2)
    with pytest.raises(AssertionError):
        bf.add_enums(EnumValue('enum_a', 8, 'Enum A'))


def test_enum_unique():
    """All enums must be unique"""
    # name
    bf = BitField('bf_a', 'Bit field A', width=8)
    bf.add_enums(EnumValue('enum_a', 3, 'Enum A'))
    bf.add_enums(EnumValue('enum_b', 0, 'Enum B'))
    bf[1].name = 'enum_b'
    with pytest.raises(AssertionError):
        bf.validate()
    # value
    bf = BitField('bf_a', 'Bit field A', width=8)
    bf.add_enums(EnumValue('enum_a', 3, 'Enum A',))
    bf.add_enums(EnumValue('enum_b', 0, 'Enum B',))
    bf['enum_b'].value = 3
    with pytest.raises(AssertionError):
        bf.validate()


def test_custom_props():
    """Add custom properties on creation"""
    # init
    bf = BitField()
    assert bf.etc == {}
    bf = BitField(the_answer=42)
    assert bf.etc['the_answer'] == 42
    assert bf.as_dict()['the_answer'] == 42
