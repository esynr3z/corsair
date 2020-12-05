#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Configuration module tests.
"""

import pytest
from corsair.regmap import (
    BitField,
    Register,
    RegisterMap
)
import copy


class TestBitField:
    """Class 'Bitfield' testing."""
    def test_create(self):
        """Test of a bit field creation."""
        name = 'bf_a'
        description = ''
        initial = 0
        width = 1
        lsb = 0
        access = 'rw'
        access_flags = False
        modifiers = []
        bf = BitField(name)
        print(repr(bf))
        print(bf)
        assert (name, description, initial, width, lsb, access, access_flags, modifiers) == \
               (bf.name, bf.description, bf.initial, bf.width, bf.lsb, bf.access, bf.access_flags, bf.modifiers)

    def test_eq(self):
        """Test of equality comparision of bit fields."""
        bf1 = BitField('bf_a', initial=2)
        bf2 = copy.deepcopy(bf1)
        assert bf1 == bf2

    def test_ne(self):
        """Test of non equality comparision of bit fields."""
        bf1 = BitField('bf_a', initial=2)
        bf2 = copy.deepcopy(bf1)
        bf2 .initial = 3
        assert bf1 != bf2

    def test_initial_access(self):
        """Test of accessing to 'initial' attribute of a bit field."""
        bf = BitField('bf_a')
        bf.initial = 2
        assert bf.initial == 2

    def test_initial_init_wrong(self):
        """Test of initializing a bit field with a wrong 'initial' value."""
        with pytest.raises(ValueError):
            BitField('bf_a', initial=0.0)

    def test_initial_set_wrong(self):
        """Test of setting wrong value to 'initial' attribute of a bit field."""
        bf = BitField('bf_a')
        with pytest.raises(ValueError):
            bf.initial = 0.0

    def test_width_access(self):
        """Test of accessing to 'width' attribute of a bit field."""
        bf = BitField('bf_a')
        bf.width = 16
        assert bf.width == 16

    def test_width_init_wrong(self):
        """Test of initializing a bit field with a wrong 'width' value."""
        with pytest.raises(ValueError):
            BitField('bf_a', width='0')

    def test_width_set_wrong(self):
        """Test of setting wrong value to 'width' attribute of a bit field."""
        bf = BitField('bf_a')
        with pytest.raises(ValueError):
            bf.width = 0

    def test_lsb_access(self):
        """Test of accessing to 'lsb' attribute of a bit field."""
        bf = BitField('bf_a')
        bf.lsb = 3
        assert bf.lsb == 3

    def test_lsb_init_wrong(self):
        """Test of initializing a bit field with a wrong 'lsb' value."""
        with pytest.raises(ValueError):
            BitField('bf_a', lsb='3')

    def test_lsb_set_wrong(self):
        """Test of setting wrong value to 'lsb' attribute of a bit field."""
        bf = BitField('bf_a')
        with pytest.raises(ValueError):
            bf.lsb = -1

    def test_msb_access(self):
        """Test of accessing to 'msb' attribute of a bit field."""
        bf = BitField('bf_a', lsb=2, width=4)
        assert bf.msb == 5

    def test_access_access(self):
        """Test of accessing to 'access' attribute of a bit field."""
        bf = BitField('bf_a')
        bf.access = 'wo'
        assert bf.access == 'wo'

    def test_access_init_wrong(self):
        """Test of initializing a bit field with a wrong 'access' value."""
        with pytest.raises(ValueError):
            BitField('bf_a', access='w0')

    def test_access_set_wrong(self):
        """Test of setting wrong value to 'access' attribute of a bit field."""
        bf = BitField('bf_a')
        with pytest.raises(ValueError):
            bf.access = 'wr'

    def test_access_flags_access(self):
        """Test of accessing to 'access_flags' attribute of a bit field."""
        bf = BitField('bf_a')
        bf.access_flags = True
        assert bf.access_flags is True

    def test_access_flags_init_wrong(self):
        """Test of initializing a bit field with a wrong 'access_flags' value."""
        with pytest.raises(ValueError):
            BitField('bf_a', access_flags='true')

    def test_access_flags_set_wrong(self):
        """Test of setting wrong value to 'access_flags' attribute of a bit field."""
        bf = BitField('bf_a')
        with pytest.raises(ValueError):
            bf.access_flags = 0

    def test_modifiers_access(self):
        """Test of accessing to 'modifiers' attribute of a bit field."""
        bf = BitField('bf_a', access='rw')
        bf.modifiers = ['external_update']
        assert bf.modifiers == ['external_update']

    def test_modifiers_init_wrong(self):
        """Test of initializing a bit field with a wrong 'modifiers' value."""
        with pytest.raises(ValueError):
            BitField('bf_a', access='wo', modifiers=['external_update', 'read_to_clear'])

    def test_modifiers_set_wrong(self):
        """Test of setting wrong value to 'modifiers' attribute of a bit field."""
        bf = BitField('bf_a', access='ro')
        with pytest.raises(ValueError):
            bf.modifiers = 'self_clear'


class TestRegister:
    """Class 'Register' testing."""
    def test_create(self):
        """Test of a register creation."""
        name = 'reg_a'
        description = 'Register A'
        address = 0x4
        bfields = [BitField('bf_a', 'Bit field A'), BitField('bf_b', 'Bit field B')]
        reg = Register(name, description, address)
        reg.add_bfields(bfields)
        print(repr(reg))
        print(reg)
        assert (name, description, address, bfields) == \
               (reg.name, reg.description, reg.address, reg.bfields)

    def test_eq(self):
        """Test of equality comparision of registes."""
        reg1 = Register()
        reg1.add_bfields([BitField('bf_a', 'Bit field A'), BitField('bf_b', 'Bit field B')])
        reg2 = copy.deepcopy(reg1)
        assert reg1 == reg2

    def test_ne(self):
        """Test of non equality comparision of registers."""
        reg1 = Register()
        reg1.add_bfields([BitField('bf_a', 'Bit field A'), BitField('bf_b', 'Bit field B')])
        reg2 = copy.deepcopy(reg1)
        reg2['bf_a'].access = 'wo'
        assert reg1 != reg2

    def test_name_error_no_fields(self):
        """Test of a register creation with no name and no fields."""
        reg = Register()
        with pytest.raises(ValueError):
            reg.name

    def test_name_error_with_fields(self):
        """Test of a register creation with no name and several fields."""
        reg = Register()
        reg.add_bfields([BitField('bf_a', 'Bit field A'), BitField('bf_b', 'Bit field B')])
        with pytest.raises(ValueError):
            reg.name

    def test_name_of_field(self):
        """Test of a register with name and description of the field."""
        reg = Register()
        reg.add_bfields(BitField('CNT', 'Counter'))
        print(reg.name, reg.description)
        print(reg[0].name, reg.description)
        print(reg[0].name, reg[0].description)
        assert reg.name == reg[0].name and \
               reg.description == reg[0].description

    def test_add_field(self):
        """Test of adding field to a register."""
        reg = Register('REGA', 'Register A')
        bf = BitField('bf_a', 'Bit field A')
        reg.add_bfields(bf)
        assert bf == reg['bf_a'] and bf == reg[0]

    def test_add_fields(self):
        """Test of adding several fields to a register"""
        reg = Register('REGA', 'Register A')
        bf = [BitField('bf_a', 'Bit field A'), BitField('bf_b', 'Bit field B')]
        reg.add_bfields(bf)
        assert bf[0] == reg['bf_a'] and bf[0] == reg[0] and \
               bf[1] == reg['bf_b'] and bf[1] == reg[1]

    def test_get_field_key_error(self):
        """Test of trying to get bit field with wrong name."""
        reg = Register('REGA', 'Register A')
        bf = [BitField('bf_a', 'Bit field A'), BitField('bf_b', 'Bit field B')]
        reg.add_bfields(bf)
        with pytest.raises(KeyError):
            reg['bf_c']

    def test_get_field_index_error(self):
        """Test of trying to get bit field with wrong index."""
        reg = Register('REGA', 'Register A')
        bf = [BitField('bf_a', 'Bit field A'), BitField('bf_b', 'Bit field B')]
        reg.add_bfields(bf)
        with pytest.raises(KeyError):
            reg[3]


class TestRegisterMap:
    """Class 'RegisterMap' testing."""
    def test_create(self):
        """Test of a register map creation."""
        name = 'reg_a'
        description = 'Register A'
        address = 0x4
        reg = Register(name, description, address)
        reg.add_bfields([
            BitField('bf_a', 'Bit field A'),
            BitField('bf_b', 'Bit field B')
        ])
        rmap = RegisterMap()
        rmap.add_regs(reg)

        print(repr(rmap))
        print(rmap)
        assert rmap['reg_a'] == reg

    def test_eq(self):
        """Test of equality comparision of register maps."""
        reg = Register('reg_a', 'Register A', 0x4)
        reg.add_bfields([
            BitField('bf_a', 'Bit field A'),
            BitField('bf_b', 'Bit field B')
        ])
        rmap1 = RegisterMap()
        rmap1.add_regs(reg)
        rmap2 = copy.deepcopy(rmap1)
        assert rmap1 == rmap2

    def test_ne(self):
        """Test of non equality comparision of register maps."""
        reg = Register('reg_a', 'Register A', 0x4)
        reg.add_bfields([
            BitField('bf_a', 'Bit field A'),
            BitField('bf_b', 'Bit field B')
        ])
        rmap1 = RegisterMap()
        rmap1.add_regs(reg)
        rmap2 = copy.deepcopy(rmap1)
        rmap2['reg_a']['bf_b'].initial = 1
        assert rmap1 != rmap2
