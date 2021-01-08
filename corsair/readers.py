#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""File readers.
"""

import json
import yaml
from .config import Configuration
from .regmap import BitField, Register, RegisterMap
from . import utils


class _DictReader():
    """Base class that converts file to a dictionary."""
    def _open_file(self, path):
        """Read file to dictionary."""
        with open(path, 'r') as f:
            print("  Open file ... ", end='')
            ext = utils.get_file_ext(path)
            if ext in ['.yaml', '.yml']:
                data = yaml.safe_load(f)
            elif ext == '.json':
                data = json.load(f)
            else:
                raise ValueError("Unknown extension '%s' of the file '%s'" % (ext, path))
            print("OK")
        return data


class RegisterMapReader(_DictReader):
    """Read register map and configuration from file.

    Examples:

        Read provided file and create :class:`RegisterMap` object:

        >>> from corsair import RegisterMapReader
        >>> reader = RegisterMapReader()
        >>> rmap = reader('tests/data/map.json')
        Read 'tests/data/map.json' file with RegisterMapReader:
          Open file ... OK
          Read configuration ... OK
          Read registers ... OK
    """
    def __call__(self, path, config=Configuration()):
        """Read input file.

        Returns:
            :class:`RegisterMap` object.
        """
        print("Read '%s' file with RegisterMapReader:" % path)
        data = self._open_file(path)

        # Read configuration
        print("  Read configuration ... ", end='')
        if 'config' in data.keys():
            config.values = data['config']
            print("OK")
        else:
            print("Not provided")

        # Read registers
        print("  Read registers ... ", end='')
        rmap = RegisterMap(config=config)
        for data_reg in data['regmap']:
            data_reg_filtered = {k: v for k, v in data_reg.items() if k in ['name', 'description', 'address']}
            reg = Register(**data_reg_filtered)
            for data_bf in data_reg['bfields']:
                reg.add_bfields(BitField(**data_bf))
            rmap.add_regs(reg)
        print("OK")
        return rmap


class ConfigurationReader(_DictReader):
    """Read configuration from file.

    Examples:
        Read provided file and create :class:`Configuration` object:

        >>> from corsair import ConfigurationReader
        >>> reader = ConfigurationReader()
        >>> rmap = reader('tests/data/config.json')
        Read 'tests/data/config.json' file with ConfigurationReader:
          Open file ... OK
          Read configuration ... OK
    """
    def __call__(self, path):
        """Read input file.

        Returns:
            :class:`Configuration` object.
        """
        print("Read '%s' file with ConfigurationReader:" % path)
        data = self._open_file(path)
        print("  Read configuration ... ", end='')
        config = Configuration()
        config.values = data
        print("OK")
        return config
