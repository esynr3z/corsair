#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Register map.
"""

from . import utils
from .config import Configuration


class BitField():
    """Bit field.

    Examples:

        Create a bit field:

        >>> print(BitField('bf_a', 'bf_a description', lsb=0, width=8))
        bf_a: bf_a description
          initial = 0
          width = 8
          lsb = 0
          access = rw
          access_flags = False
          modifiers = []

    Attributes:
        name: Name of the bit field.
        description: Description of the bit field.
    """
    def __init__(self, name, description='', initial=0, width=1,
                 lsb=0, access='rw', access_flags=False, modifiers=[]):
        self.name = name
        self.description = description
        self.initial = initial
        self.width = width
        self.lsb = lsb
        self.access = access
        self.access_flags = access_flags
        self.modifiers = modifiers

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

    def as_str(self, indent=''):
        """Returns indented string with the bit field information."""
        inner_indent = indent + '  '
        bf_str = indent + '%s: %s\n' % (self.name, self.description)
        bf_str += inner_indent + 'initial = %s\n' % utils.try_int_to_str(self.initial)
        bf_str += inner_indent + 'width = %s\n' % self.width
        bf_str += inner_indent + 'lsb = %s\n' % self.lsb
        bf_str += inner_indent + 'access = %s\n' % self.access
        bf_str += inner_indent + 'access_flags = %s\n' % self.access_flags
        bf_str += inner_indent + 'modifiers = %s' % self.modifiers
        return bf_str

    def as_dict(self):
        """Returns dictionary with bit field's key attributes."""
        return {
            'name': self.name,
            'description': self.description,
            'initial': self.initial,
            'width': self.width,
            'lsb': self.lsb,
            'access': self.access,
            'access_flags': self.access_flags,
            'modifiers': self.modifiers
        }

    @property
    def initial(self):
        """Initial value for the field. Only non-negative integers are allowed."""
        return self._initial

    @initial.setter
    def initial(self, value):
        value = utils.try_hex_to_dec(value)
        err_msg = ("Initial value '%s' for '%s' is wrong!"
                   " Only non-negative integers are allowed." % (value, self.name))
        if utils.is_non_neg_int(value, err_msg):
            self._initial = value

    @property
    def width(self):
        """Bit width of the field. Only positive integers are allowed."""
        return self._width

    @width.setter
    def width(self, value):
        value = utils.try_hex_to_dec(value)
        err_msg = ("Width value '%s' for '%s' is wrong!"
                   " Only positive integers are allowed." % (value, self.name))
        if utils.is_pos_int(value, err_msg):
            self._width = value

    @property
    def lsb(self):
        """Position of less significant bit (LSB) of the field. Only non-negative integers are allowed."""
        return self._lsb

    @lsb.setter
    def lsb(self, value):
        value = utils.try_hex_to_dec(value)
        err_msg = ("LSB value '%s' for '%s' is wrong!"
                   " Only non-negative integers are allowed." % (value, self.name))
        if utils.is_non_neg_int(value, err_msg):
            self._lsb = value

    @property
    def msb(self):
        """Position of most significant bit (MSB) of the field."""
        return self.lsb + self.width - 1

    @property
    def access(self):
        """Bit field access mode."""
        return self._access

    @access.setter
    def access(self, value):
        if value not in ['rw', 'ro', 'wo']:
            raise ValueError("Unknown access mode '%s' for '%s' field!" % (value, self.name))
        else:
            self._access = value

    @property
    def access_flags(self):
        """Enable access flags generation."""
        return self._access_flags

    @access_flags.setter
    def access_flags(self, value):
        if isinstance(value, bool):
            self._access_flags = value
        else:
            raise ValueError("Access flags attribute has to be 'bool', "
                             "but '%s' provided for '%s' field!" % (type(value), self.name))

    @property
    def modifiers(self):
        """List of an access modifiers."""
        return self._modifiers

    @modifiers.setter
    def modifiers(self, value):
        # hack to handle single elements
        if type(value) is not list:
            value = [value]

        # check if all options are allowed
        allowlist = [
            'self_clear',
            'write1_to_clear',
            'write1_to_toggle',
            'read_to_clear',
            'read_const',
            'external_update',
            'memory'
        ]
        for v in value:
            if v not in allowlist:
                raise ValueError("Unknown access mode '%s' for '%s' field!" % (v, self.name))

        # check if options combination is allowed
        allowlist_comb = {
            'rw': [
                [],
                ['external_update'],
                ['external_update', 'write1_to_clear'],
                ['external_update', 'write1_to_toggle'],
                ['memory']
            ],
            'wo': [
                [],
                ['self_clear'],
                ['memory']
            ],
            'ro': [
                [],
                ['read_const'],
                ['external_update'],
                ['external_update', 'read_to_clear'],
                ['memory']
            ],
        }
        if value not in allowlist_comb[self.access]:
            raise ValueError("Unknown access modifiers combination '%s' for '%s' field!" % (value, self.name))

        self._modifiers = value

    @property
    def bits(self):
        """Returns list with all bits positions used by a bit field"""
        return list(range(self.lsb, self.msb + 1))


class Register():
    """Control and status register.

    Examples:

        Create a register:

        >>> reg = Register('reg_a', 'Register A description', address=8)
        >>> reg.add_bfields([
        ...     BitField('bf_a', 'Bit field A', lsb=0),
        ...     BitField('bf_b', 'Bit field B', lsb=1)
        ... ])
        >>> print(reg)
        (0x8) reg_a: Register A description
          bf_a: Bit field A
            initial = 0
            width = 1
            lsb = 0
            access = rw
            access_flags = False
            modifiers = []
          bf_b: Bit field B
            initial = 0
            width = 1
            lsb = 1
            access = rw
            access_flags = False
            modifiers = []

        Access bit field via name or index:

        >>> reg = Register('reg_a', 'Register A description', address=8)
        >>> reg.add_bfields([
        ...     BitField('bf_a', 'Bit field A', lsb=0),
        ...     BitField('bf_b', 'Bit field B', lsb=1)
        ... ])
        >>> print(reg['bf_b'].name, reg[1].name)
        bf_b bf_b

        Iterate through bit fields:

        >>> reg = Register('reg_a', 'Register A description', address=8)
        >>> reg.add_bfields([
        ...     BitField('bf_a', 'Bit field A', lsb=0),
        ...     BitField('bf_b', 'Bit field B', lsb=1)
        ... ])
        >>> for bf in reg:
        ...     print(bf.name)
        ...
        bf_a
        bf_b
    """
    def __init__(self, name='', description='', address=None):
        self._bfields = []

        self.name = name
        self.description = description
        self.address = address

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
        """Returns indented string with the register information."""
        inner_indent = indent + '  '
        bfields = [bf.as_str(inner_indent) for bf in self.bfields]
        bfields_str = '\n'.join(bfields) if bfields else inner_indent + 'empty'
        return indent + '(0x%x) %s: %s\n' % (self.address, self.name, self.description) + bfields_str

    def as_dict(self):
        """Returns dictionary with register's key attributes."""
        return {
            'name': self.name,
            'description': self.description,
            'address': self.address,
            'bit_fields': [bf.as_dict() for bf in self.bfields]
        }

    def __len__(self):
        """Number of register's bit fields."""
        return len(self._bfields)

    def __iter__(self):
        """Bit fields iterator."""
        return iter(self._bfields)

    def __getitem__(self, key):
        """Get bit field by name or index.

        Raises:
            KeyError: An error occured if bit field does not exists.
        """
        try:
            if isinstance(key, str):
                return next(bf for bf in self if bf.name == key)
            else:
                return self._bfields[key]
        except (StopIteration, TypeError, KeyError, IndexError):
            raise KeyError("There is no bit field with a name/index '%s' in '%s' register!" % (key, self.name))

    def __setitem__(self, key, value):
        """Set bit field by key"""
        raise KeyError("Not able to set '%s' bit field directly in '%s' register!"
                       " Try use add_bfields() method." % (key, self.name))

    @property
    def name(self):
        """Register name. If name is not set, use name of the first field."""
        if not self._name:
            if len(self) == 0:
                raise ValueError("Register has no name and no fields!")
            elif len(self) > 1:
                raise ValueError("Register has %d fields but has no name!" % len(self))
            else:
                return self[0].name
        else:
            return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def address(self):
        """Register address. Only non-negative integers are allowed."""
        return self._address

    @address.setter
    def address(self, value):
        value = utils.try_hex_to_dec(value)
        err_msg = ("Address value '%s' for '%s' is wrong!"
                   " Only non-negative integers are allowed." % (value, self._name))
        if value is None:
            self._address = None
        elif utils.is_non_neg_int(value, err_msg):
            self._address = value

    @property
    def names(self):
        """Return all bit field names"""
        return [bf.name for bf in self]

    @property
    def description(self):
        """Register description.If description is not set, use description of the first field."""
        if not self._description and len(self) == 1:
            return self[0].description
        else:
            return self._description

    @description.setter
    def description(self, value):
        self._description = value

    @property
    def bfields(self):
        """Returns list with bit field objects."""
        return self._bfields

    def add_bfields(self, new_bfields):
        """Add bit field or list of bit feilds.

        Bit fields are automatically sorted and stored in the ascending order of msb attributes.
        """
        # hack to handle single elements
        new_bfields = utils.listify(new_bfields)

        # add bit fields to list one by one
        for bf in new_bfields:
            # check existance
            if bf.name in self.names:
                raise ValueError("Bit field with name '%s' is already present in '%s' register!" % (bf.name, self.name))
            # check fields overlapping
            overlaps = [set(bf.bits).intersection(set(old_bf.bits)) for old_bf in self._bfields]
            overlaps_names = [self.names[i] for i, ovl in enumerate(overlaps) if ovl]
            if self.bfields and overlaps_names:
                raise ValueError("Position of a bit field '%s'"
                                 " conflicts with other bit field(s): %s!" % (bf.name, repr(overlaps_names)))
            # if we here - all is ok and bit field can be added
            try:
                # find position to insert bit field and not to break ascending order of bit field msb positions
                bf_idx = next(i for i, old_bf in enumerate(self._bfields) if old_bf.msb > bf.msb)
                self._bfields.insert(bf_idx, bf)
            except StopIteration:
                # when bit field list is empty or all bit field msb positions are less than the current one
                self._bfields.append(bf)


class RegisterMap():
    """CSR map.

    Examples:

        Create a register map:

        >>> rmap = RegisterMap()
        >>> rmap.add_regs([
        ...     Register('reg_a', 'Register A', address=0),
        ...     Register('reg_b', 'Register B', address=4)
        ... ])
        >>> print(rmap)
        register_map: v1.0
          (0x0) reg_a: Register A
            empty
          (0x4) reg_b: Register B
            empty

        Access register via name or index:

        >>> rmap = RegisterMap()
        >>> rmap.add_regs([
        ...     Register('reg_a', 'Register A', address=0),
        ...     Register('reg_b', 'Register B', address=4)
        ... ])
        >>> print(rmap['reg_a'].name, rmap[0].name)
        reg_a reg_a

        Iterate through registers:

        >>> rmap = RegisterMap()
        >>> rmap.add_regs([
        ...     Register('reg_a', 'Register A', address=0),
        ...     Register('reg_b', 'Register B', address=4)
        ... ])
        >>> for reg in rmap:
        ...     print(reg.name)
        ...
        reg_a
        reg_b

    Attributes:
        name: Name of a map.
        version: Version of a map.
    """
    def __init__(self, name='register_map', version='1.0', config=Configuration()):
        self.name = name
        self.version = version
        self.config = config
        self._regs = []

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
        return 'RegisterMap(%s, %s, %s)' % (repr(self.name), repr(self.version), repr(self.config))

    def __str__(self):
        return self.as_str()

    def as_str(self, indent=''):
        """Returns indented string with the register map information."""
        inner_indent = indent + '  '
        regs = [reg.as_str(inner_indent) for reg in self.regs]
        regs_str = '\n'.join(regs) if regs else inner_indent + 'empty'
        return indent + '%s: v%s\n' % (self.name, self.version) + regs_str

    def as_dict(self):
        """Returns register map as a dictionary."""
        return {reg.name: reg.as_dict() for reg in self.regs}

    def __len__(self):
        """Number of registers."""
        return len(self._regs)

    def __iter__(self):
        """Registers iterator."""
        return iter(self._regs)

    def __getitem__(self, key):
        """Get register by name or index.

        Raises:
            KeyError: An error occured if register does not exists.
        """
        try:
            if isinstance(key, str):
                return next(reg for reg in self if reg.name == key)
            else:
                return self._regs[key]
        except (StopIteration, TypeError, KeyError, IndexError):
            raise KeyError("There is no register with a name/index '%s'!" % (key))

    def __setitem__(self, key, value):
        """Set register by key"""
        raise KeyError("Not able to set '%s' register directly!"
                       " Try use add_regs() method." % (key))

    @property
    def names(self):
        """Return all register names."""
        return [reg.name for reg in self]

    def _addr_apply(self, reg):
        """Apply auto-calculated address for a register with no address."""
        # some error checks
        if len(self) == 0:
            raise ValueError("Register '%s' with no address is not allowed"
                             " to be the first register in a map!" % (reg.name))
        if self.config['address_calculation']['auto_increment_mode'].value == 'none':
            raise ValueError("Register '%s' with no address is not allowed"
                             " when address auto increment is disabled!" % (reg.name))

        prev_addr = self.regs[-1].address

        if self.config['address_calculation']['auto_increment_mode'].value == 'data_width':
            addr_step = self.config['interface_generic']['data_width'].value // 8
        else:
            addr_step = self.config['address_calculation']['auto_increment_value'].value

        reg.address = prev_addr + addr_step

    def _addr_check(self, reg):
        """Check address alignment."""
        if self.config['address_calculation']['alignment_mode'].value == 'data_width':
            align_val = self.config['interface_generic']['data_width'].value // 8
        elif self.config['address_calculation']['alignment_mode'].value == 'custom':
            align_val = self.config['address_calculation']['alignment_value'].value
        else:
            align_val = 1

        if (reg.address % align_val) != 0:
            raise ValueError("Register '%s' with address '%d' is not %d bytes alligned!" %
                             (reg.name, reg.address, align_val))

    @property
    def regs(self):
        """Returns list with register objects."""
        return self._regs

    def add_regs(self, new_regs):
        """Add register or list of registers.

        Register are automatically sorted and stored in the ascending order of addresses.
        """
        # hack to handle single elements
        new_regs = utils.listify(new_regs)

        # add registers to list one by one
        for reg in new_regs:
            # check existance
            if reg.name in self.names:
                raise ValueError("Register with name '%s' is already present!" % (reg.name))
            # check bit field conflicts with data width
            for bf in reg:
                if bf.msb >= self.config['interface_generic']['data_width'].value:
                    raise ValueError("Register '%s' has field '%s' (msb=%d) "
                                     "that exceeds interface data width %d!" %
                                     (reg.name, bf.name, bf.msb, self.config['interface_generic']['data_width'].value))
            # aplly calculated address if register address is empty
            if reg.address is None:
                self._addr_apply(reg)
            # check address alignment
            self._addr_check(reg)
            # check address conflicts
            addresses = [reg.address for reg in self]
            if reg.address in addresses:
                conflict_reg = self[addresses.index(reg.address)].name
                raise ValueError("Register '%s' with address '%d'"
                                 " conflicts with register '%s' with the same address!" %
                                 (reg.name, reg.address, conflict_reg))
            # if we here - all is ok and register can be added
            try:
                # find position to insert register and not to break ascending order of addresses
                reg_idx = next(i for i, r in enumerate(self._regs) if r.address > reg.address)
                self._regs.insert(reg_idx, reg)
            except StopIteration:
                # when registers list is empty or all addresses are less than the current one
                self._regs.append(reg)
