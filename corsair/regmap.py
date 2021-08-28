#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Register map
"""

from . import utils
from . import config
from .reg import Register
from .bitfield import BitField
from .enum import EnumValue
import json
import yaml


class RegisterMap():
    """CSR map"""

    def __init__(self):
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
        return 'RegisterMap()'

    def __str__(self):
        return self.as_str()

    def as_str(self, indent=''):
        """Create indented string with the information about register map."""
        inner_indent = indent + '  '
        regs = [reg.as_str(inner_indent) for reg in self.regs]
        regs_str = '\n'.join(regs) if regs else inner_indent + 'empty'
        return indent + 'register map:\n' + regs_str

    def as_dict(self):
        """Return register map as a dictionary."""
        return {reg.name: reg.as_dict() for reg in self.regs}

    def __len__(self):
        """Calculate number of the registers"""
        return len(self._regs)

    def __iter__(self):
        """Create iterator over registers"""
        return iter(self._regs)

    def __getitem__(self, key):
        """Get register by name or index"""
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
                       " Try use add_registers() method." % (key))

    @property
    def reg_names(self):
        """List with all register names."""
        return [reg.name for reg in self]

    def _addr_resolve(self, reg):
        """Resolve address for a register with no address."""
        # some error checks
        assert len(self) != 0, \
            "Register '%s' with no address is not allowed to be the first register in a map!" % (reg.name)
        assert config.globcfg['address_increment'] != 'none', \
            "Register '%s' with no address is not allowed when address auto increment is disabled!" % (reg.name)

        prev_addr = self.regs[-1].address

        if config.globcfg['address_increment'] == 'data_width':
            addr_step = config.globcfg['data_width'] // 8
        else:
            addr_step = config.globcfg['address_increment']

        reg.address = prev_addr + addr_step

    def _addr_check_alignment(self, reg):
        """Check address alignment."""
        if config.globcfg['address_alignment'] == 'none':
            align_val = 1
        elif config.globcfg['address_alignment'] == 'data_width':
            align_val = config.globcfg['data_width'] // 8
        else:
            align_val = config.globcfg['address_alignment']

        assert (reg.address % align_val) == 0, \
            "Register '%s' with address '%d' is not %d bytes alligned!" % (reg.name, reg.address, align_val)

    def _addr_check_conflicts(self, reg):
        addresses = [reg.address for reg in self]
        if reg.address in addresses:
            conflict_reg = self[addresses.index(reg.address)]
            assert False, "Register '%s' with address '%d' conflicts with register '%s' with the same address!" % \
                (reg.name, reg.address, conflict_reg.name)

    @property
    def regs(self):
        """List with register objects."""
        return self._regs

    def add_registers(self, new_regs):
        """Add list of registers.

        Register are automatically sorted and stored in the ascending order of addresses.
        """
        # hack to handle single elements
        new_regs = utils.listify(new_regs)

        # add registers to the list one by one
        for reg in new_regs:
            # check existance
            assert reg.name not in self.reg_names, \
                "Register with name '%s' is already present!" % (reg.name)
            # aplly calculated address if register address is empty
            if reg.address is None:
                self._addr_resolve(reg)
            # check address alignment
            self._addr_check_alignment(reg)
            # check address conflicts
            self._addr_check_conflicts(reg)
            # if we here - all is ok and register can be added
            try:
                # find position to insert register and not to break ascending order of addresses
                reg_idx = next(i for i, r in enumerate(self._regs) if r.address > reg.address)
                self._regs.insert(reg_idx, reg)
            except StopIteration:
                # when registers list is empty or all addresses are less than the current one
                self._regs.append(reg)
        return self

    def validate(self):
        """Validate the register map."""
        for reg in self.regs:
            assert self.reg_names.count(reg.name) == 1, \
                "Register '%s' name is not unique!" % (reg.name)
            reg.validate()

    def read_file(self, path):
        """Read register map from file (based on extension)."""
        ext = utils.get_file_ext(path)
        if ext in ['.yaml', '.yml']:
            self.read_yaml(path)
        elif ext == '.json':
            self.read_json(path)
        elif ext == '.txt':
            self.read_txt(path)
        else:
            raise ValueError("Unknown extension '%s' of the file '%s'" % (ext, path))

    def read_json(self, path):
        """Read register map from JSON file."""
        with open(path, 'r') as f:
            data = json.load(f)
            self._fill_from_file_data(data['regmap'])

    def read_yaml(self, path):
        """Read register map from YAML file."""
        with open(path, 'r') as f:
            data = yaml.safe_load(f)
            self._fill_from_file_data(data['regmap'])

    def read_txt(self, path):
        """Read register map from text file."""
        with open(path, 'r') as f:
            raw_lines = f.readlines()
            data = []
            reg_start_idx = None
            for i, line in enumerate(raw_lines):
                if '-----' in line:
                    reg_start_idx = i + 1
                if reg_start_idx and i >= reg_start_idx:
                    # register with one bitfield template
                    reg = {"name": None, "description": None,
                           "bitfields": [{"width": None, "access": None, "hardware": None}]}
                    # prepare the line
                    line_data = [s.strip() for s in line.split("|")[1:-1]]
                    if len(line_data) != 7:
                        raise ValueError("Not enough / too much columns in line %d. Plese fix!" % (i + 1))
                    # extract register properties
                    if line_data[0]:  # address value can be ommited
                        reg["address"] = line_data[0]
                    reg["address"] = line_data[0] if line_data[0] else None
                    reg["name"] = line_data[1]
                    reg["bitfields"][0]["width"] = line_data[2]
                    reg["bitfields"][0]["access"] = line_data[3]
                    reg["bitfields"][0]["hardware"] = line_data[4]
                    if line_data[4]:  # reset value can be ommited
                        reg["bitfields"][0]["reset"] = line_data[5]
                    reg["description"] = line_data[6]
                    data.append(reg)
            if not reg_start_idx:
                raise ValueError("Can't find table with registers!")
            self._fill_from_file_data(data)

    def _fill_from_file_data(self, data):
        """Fill register map with data from file."""
        self._regs = []
        for data_reg in data:
            data_reg_filtered = {k: v for k, v in data_reg.items() if k != 'bitfields'}
            reg = Register(**data_reg_filtered)
            for data_bf in data_reg['bitfields']:
                data_bf_filtered = {k: v for k, v in data_bf.items() if k != 'enums'}
                bf = BitField(**data_bf_filtered)
                if 'enums' in data_bf.keys():
                    for data_enum in data_bf['enums']:
                        bf.add_enums(EnumValue(**data_enum))
                reg.add_bitfields(bf)
            self.add_registers(reg)
