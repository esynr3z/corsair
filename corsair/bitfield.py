#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Bit field inside register
"""

from . import utils
from . import config


class BitField():
    """Bit field.

    :param name: Bit field name
    :type name: str
    :param description: Bit field description
    :type description: str
    :param reset: Bit field reset vaue
    :type reset: int
    :param width: Bit field width vaue
    :type width: int
    :param lsb: Bit field LSB vaue
    :type lsb: int
    :param access: Bit field access mode
    :type access: str
    :param hardware: Bit field hardware options
    :type hardware: str
    """

    def __init__(self, name='val', description='Value of the register', reset=0, width=1,
                 lsb=0, access='rw', hardware='n', **args):
        self._enums = []

        self.name = name
        self.description = description
        self.reset = utils.str2int(reset)
        self.width = utils.str2int(width)
        self.lsb = utils.str2int(lsb)
        self.access = access
        self.hardware = hardware
        self.etc = args

    def __eq__(self, other):
        if self.__class__ != other.__class__:
            raise TypeError("Failed to compare '%s' with '%s'!" % (repr(self), repr(other)))
        else:
            return self.as_dict() == other.as_dict()

    def __ne__(self, other):
        if self.__class__ != other.__class__:
            raise TypeError("Failed to compare '%s' with '%s'!" % (repr(self), repr(other)))
        else:
            return not self.__eq__(other)

    def __repr__(self):
        return 'BitField(%s)' % repr(self.name)

    def __str__(self):
        return self.as_str()

    def __len__(self):
        """Calculate number of enums inside bitfield"""
        return len(self._enums)

    def __iter__(self):
        """Create iterator over enums"""
        return iter(self._enums)

    def __getitem__(self, key):
        """Get enum by name or index."""
        try:
            if utils.is_str(key):
                key = utils.force_name_case(key)
                return next(enum for enum in self if enum.name == key)
            else:
                return self._enums[key]
        except (StopIteration, TypeError, KeyError, IndexError):
            raise KeyError("There is no enum with the name/index '%s' in the '%s' bitfield!" % (key, self.name))

    def __setitem__(self, key, value):
        """Set enum by key"""
        raise KeyError("Not able to set '%s' enum directly in the '%s' bit field!"
                       " Try to use add_enums() method." % (key, self.name))

    def as_str(self, indent=''):
        """Create an indented string with the bit field information."""
        inner_indent = indent + '  '
        bf_str = indent + '%s: %s\n' % (self.name, self.description)
        bf_str += inner_indent + 'reset = %s\n' % utils.int2str(self.reset)
        bf_str += inner_indent + 'width = %s\n' % self.width
        bf_str += inner_indent + 'lsb = %s\n' % self.lsb
        bf_str += inner_indent + 'access = %s\n' % self.access
        bf_str += inner_indent + 'hardware = %s\n' % self.hardware
        bf_str += inner_indent + 'enums:\n'
        enums = [enum.as_str(inner_indent + inner_indent) for enum in self.enums]
        bf_str += '\n'.join(enums) if enums else inner_indent + 'empty'
        return bf_str

    def as_dict(self):
        """Create a dictionary with the key attributes of the bit field."""
        d = {
            'name': self.name,
            'description': self.description,
            'reset': self.reset,
            'width': self.width,
            'lsb': self.lsb,
            'access': self.access,
            'hardware': self.hardware,
            'enums': [enum.as_dict() for enum in self.enums]
        }
        d.update(self.etc)
        return d

    @property
    def name(self):
        """Name of the bit field."""
        return utils.force_name_case(self._name)

    @name.setter
    def name(self, value):
        if not utils.is_str(value):
            raise ValueError("'name' attribute has to be 'str', but '%s' provided for the bitfield!" % type(value))
        self._name = value

    @property
    def description(self):
        """Description of the bitfield."""
        return self._description

    @description.setter
    def description(self, value):
        if not utils.is_str(value):
            raise ValueError("'description' attribute has to be 'str', but '%s' provided for '%s' bitfield!" %
                             (type(value), self.name))
        self._description = value

    @property
    def reset(self):
        """Inital value of the bitfield."""
        return self._reset

    @reset.setter
    def reset(self, value):
        self._reset = utils.str2int(value)

    @property
    def lsb(self):
        """LSB value of the bitfield."""
        return self._lsb

    @lsb.setter
    def lsb(self, value):
        self._lsb = utils.str2int(value)

    @property
    def width(self):
        """Width value of the bitfield."""
        return self._width

    @width.setter
    def width(self, value):
        self._width = utils.str2int(value)

    @property
    def access(self):
        """Access mode for the bitfield."""
        return self._access

    @access.setter
    def access(self, value):
        if not utils.is_str(value):
            raise ValueError("'access' attribute has to be 'str', but '%s' provided for '%s' bitfield!" %
                             (type(value), self.name))
        self._access = value

    @property
    def hardware(self):
        """Hardware mode for the bitfield."""
        return self._hardware

    @hardware.setter
    def hardware(self, value):
        value = value.lower()
        for ch in value:
            if ch not in "iocselaqfn":
                raise ValueError("Unknown attribute '%s' for 'hardware' property of the '%s' bitfield!" %
                                 (ch, self.name))
        self._hardware = value

    @property
    def msb(self):
        """Position of most significant bit (MSB) of the field."""
        return self.lsb + self.width - 1

    @property
    def byte_strobes(self):
        """Dictionary with LSB and MSB values for the every byte in the write data bus."""
        strb = {}
        first = self.lsb // 8
        last = self.msb // 8
        for i in range(first, last + 1):
            # per every byte strobe
            wdata_lsb = self.lsb if i == first else i * 8
            wdata_msb = (i + 1) * 8 - 1 if ((i + 1) * 8 - 1 - self.msb) < 0 else self.msb
            bf_lsb = wdata_lsb - self.lsb
            bf_msb = wdata_msb - self.lsb
            strb[i] = {'bf_lsb': bf_lsb, 'bf_msb': bf_msb,
                       'wdata_lsb': wdata_lsb, 'wdata_msb': wdata_msb}
        return strb

    @property
    def enum_names(self):
        """List with all enum names."""
        return [enum.name for enum in self]

    @property
    def enums(self):
        """List with enum objects."""
        return self._enums

    def add_enums(self, new_enums):
        """Add enum or list of enums.

        Enums are automatically sorted and stored in the ascending order of value attributes.
        """
        # hack to handle single elements
        new_enums = utils.listify(new_enums)

        # add enums to list one by one
        for enum in new_enums:
            # check existance
            assert enum.name not in self.enum_names, \
                "Enum with name '%s' is already present in '%s' bitfield!" % (enum.name, self.name)
            # check enum value is unique
            assert enum.value not in [enum.value for enum in self], \
                "Enum with value '%d' is already present in '%s' bitfield!" % (enum.value, self.name)
            # check enum conflicts with bitfield width
            assert enum.value.bit_length() <= self.width, \
                "Enum '%s' value %d exceeds bitfield width %d!" % (enum.name, enum.value, self.width)
            # if we are here - all is ok and enum can be added
            try:
                # find position to insert enum and not to break ascending order of enum values
                enum_idx = next(i for i, old_enum in enumerate(self._enums) if old_enum.value > enum.value)
                self._enums.insert(enum_idx, enum)
            except StopIteration:
                # when enum list is empty or all enum values are less than the current one
                self._enums.append(enum)
        return self

    @property
    def bits(self):
        """Create list with all positions of the bits represented by the bit field."""
        return list(range(self.lsb, self.msb + 1))

    @property
    def mask(self):
        """Bit mask for the field."""
        return ((2**(self.width) - 1) << self.lsb)

    def is_vector(self):
        """Check if the width of the bit field > 1."""
        return True if self.width > 1 else False

    def validate(self):
        """Validate parameters of the bit field."""
        # name
        assert self.name, "Empty bitfield name is not allowed!"
        assert utils.is_first_letter(self.name), \
            "Name value '%s' for is wrong! Must start from a letter." % (self.name)

        # reset
        assert utils.is_non_neg_int(self.reset), \
            "Reset value '%s' for '%s' is wrong! Only non-negative integers are allowed." % (self.reset, self.name)

        # width
        assert self.width, "Empty bitfield width is not allowed!"
        assert utils.is_pos_int(self.width), \
            "Width value '%s' for '%s' is wrong! Only positive integers are allowed." % (self.width, self.name)

        # lsb
        assert utils.is_non_neg_int(self.lsb), \
            "LSB value '%s' for '%s' is wrong! Only non-negative integers are allowed." % (self.lsb, self.name)

        # access
        assert self.access in ['rw', 'rw1c', 'rw1s', 'rw1t', 'ro', 'roc', 'roll', 'rolh', 'wo', 'wosc'], \
            "Unknown access mode '%s' for '%s' field!" % (self.access, self.name)

        # hardware
        if 'q' in self.hardware or 'n' in self.hardware or 'f' in self.hardware:
            assert len(self.hardware) == 1, \
                "Wrong hardware mode '%s' for field '%s'!" % (self.hardware, self.name)
        else:
            wrong_hw = list(set(self.hardware) - (set(self.hardware) & set('ioecsla')))
            assert wrong_hw == [], \
                "Wrong hardware mode(s) '%s' in '%s' for the field '%s'!" % (wrong_hw, self.hardware, self.name)
        if 'q' in self.hardware:
            q_access_allowed = ['rw', 'ro', 'wo']
            assert self.access in q_access_allowed, \
                "Hardware mode 'q' is allowed to use only with '%s'!" % (q_access_allowed)

        # enums
        for enum in self.enums:
            assert enum.value.bit_length() <= self.width, \
                "Enum '%s' value %d exceeds bitfield width %d!" % (enum.name, enum.value, self.width)
            assert self.enum_names.count(enum.name) == 1, \
                "Enum '%s' name is not unique!" % (enum.name)
            assert [e.value for e in self].count(enum.value) == 1, \
                "Enum '%s' value is not unique!" % (enum.value)
            enum.validate()
