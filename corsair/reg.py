#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Control and status register
"""

from . import utils
from . import config


class Register():
    """Control and status register.

    :param name: Bit field name
    :type name: str
    :param description: Bit field description
    :type description: str
    :param address: Register address
    :type address: int, None
    """

    def __init__(self, name='csr0', description='Control and status register 0', address=None, **args):
        self._bitfields = []

        self.name = name
        self.description = description
        self.address = address
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
        return 'Register(%s, %s, %s)' % (repr(self.name), repr(self.description), repr(self.address))

    def __str__(self):
        return self.as_str()

    def as_str(self, indent=''):
        """Create an indented string with the information about the register."""
        inner_indent = indent + '  '
        bitfields = [bf.as_str(inner_indent) for bf in self.bitfields]
        bitfields_str = '\n'.join(bitfields) if bitfields else inner_indent + 'empty'
        reg_str = indent + '(0x%x) %s: %s\n' % (self.address, self.name, self.description)
        reg_str += bitfields_str
        return reg_str

    def as_dict(self):
        """Create a dictionary with the key attributes of the register."""
        d = {
            'name': self.name,
            'description': self.description,
            'address': self.address,
            'bitfields': [bf.as_dict() for bf in self.bitfields]
        }
        d.update(self.etc)
        return d

    def __len__(self):
        """Calculate number of bit fields inside register"""
        return len(self._bitfields)

    def __iter__(self):
        """Create iterator over bit fields """
        return iter(self._bitfields)

    def __getitem__(self, key):
        """Get bit field by name or index"""
        try:
            if utils.is_str(key):
                key = utils.force_name_case(key)
                return next(bf for bf in self if bf.name == key)
            else:
                return self._bitfields[key]
        except (StopIteration, TypeError, KeyError, IndexError):
            raise KeyError("There is no bit field with the name/index '%s' in the '%s' register!" % (key, self.name))

    def __setitem__(self, key, value):
        """Set bit field by key"""
        raise KeyError("Not able to set '%s' bit field directly in the '%s' register!"
                       " Try to use add_bitfields() method." % (key, self.name))

    @property
    def name(self):
        """Name of the register."""
        return utils.force_name_case(self._name)

    @name.setter
    def name(self, value):
        if not utils.is_str(value):
            raise ValueError("'name' attribute has to be 'str', but '%s' provided for the register!" % type(value))
        self._name = value

    @property
    def address(self):
        """Address of the register."""
        return self._address

    @address.setter
    def address(self, value):
        self._address = utils.str2int(value)

    @property
    def description(self):
        """Description of the register."""
        return self._description

    @description.setter
    def description(self, value):
        if not utils.is_str(value):
            raise ValueError("'description' attribute has to be 'str', but '%s' provided for '%s' register!" %
                             (type(value), self.name))
        self._description = value

    @property
    def bitfield_names(self):
        """List with all bit field names."""
        return [bf.name for bf in self]

    @property
    def bitfields(self):
        """List with bit field objects."""
        return self._bitfields

    def add_bitfields(self, new_bitfields):
        """Add bit field or list of bit feilds.

        Bit fields are automatically sorted and stored in the ascending order of msb attributes.
        """
        # hack to handle single elements
        new_bitfields = utils.listify(new_bitfields)

        # add bit fields to list one by one
        for bf in new_bitfields:
            # check existance
            assert bf.name not in self.bitfield_names, \
                "Bit field with name '%s' is already present in '%s' register!" % (bf.name, self.name)
            # check fields overlapping
            overlaps = [set(bf.bits).intersection(set(old_bf.bits)) for old_bf in self._bitfields]
            overlaps_names = [self.bitfield_names[i] for i, ovl in enumerate(overlaps) if ovl]
            assert not (self.bitfields and overlaps_names), \
                "Position of a bit field '%s' conflicts with other bit field(s): %s!" % (bf.name, repr(overlaps_names))
            # check bit field conflicts with data width
            data_width = config.globcfg['data_width']
            assert bf.msb < data_width, \
                "Field '%s' (msb=%d) exceeds interface data width %d!" % \
                (bf.name, bf.msb, data_width)
            # if we are here - all is ok and bit field can be added
            try:
                # find position to insert bit field and not to break ascending order of bit field msb positions
                bf_idx = next(i for i, old_bf in enumerate(self._bitfields) if old_bf.msb > bf.msb)
                self._bitfields.insert(bf_idx, bf)
            except StopIteration:
                # when bit field list is empty or all bit field msb positions are less than the current one
                self._bitfields.append(bf)
        return self

    @property
    def reset(self):
        """Reset value of the refister after reset."""
        init = 0
        for bf in self:
            init |= bf.reset << bf.lsb
        return init

    @property
    def access(self):
        """Register access mode, based on bitfields."""
        accesses = list(set([bf.access for bf in self.bitfields]))
        if len(accesses) == 1:
            return accesses[0][:2]
        else:
            return 'rw'

    def validate(self):
        """Validate parameters of the register."""
        # name
        assert self.name, "Empty register name is not allowed!"
        assert utils.is_first_letter(self.name), \
            "'name' value '%s' for the register is wrong! Must start from a letter." % (self.name)

        # address
        assert utils.is_non_neg_int(self.address), \
            "Address value '%s' for '%s' is wrong! Only non-negative integers are allowed." % (self.address, self.name)

        # bit fields overlapping
        for bf in self._bitfields:
            overlaps = [set(bf.bits).intersection(set(bf_.bits)) for bf_ in self._bitfields]
            overlaps_names = [self.bitfield_names[i] for i, ovl in enumerate(overlaps) if ovl]
            overlaps_names.pop(overlaps_names.index(bf.name))
            assert not overlaps_names, \
                "Position and size of a bit field '%s' conflicts with other bit field(s): %s!" % \
                (bf.name, repr(overlaps_names))

        # bit fields vs data_width
        data_width = config.globcfg['data_width']
        for bf in self._bitfields:
            assert bf.msb < data_width, \
                "Field '%s' (msb=%d) exceeds interface data width %d!" % \
                (bf.name, bf.msb, data_width)

        # bit fields
        for bf in self.bitfields:
            assert self.bitfield_names.count(bf.name) == 1, \
                "Bitfield '%s' name is not unique!" % (bf.name)
            bf.validate()
