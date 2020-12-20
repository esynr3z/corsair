#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""File readers.
"""

import json
import yaml
from .config import Configuration
from .regmap import BitField, Register, RegisterMap
from . import utils


class _Reader():
    """Base class for readers."""
    def _open_file(self, path):
        """Read JSON/YAML file to dictionary."""
        with open(path, 'r') as f:
            print("  Open file ... ", end='')
            ext = utils.get_file_ext(path)
            if ext in ['.yaml', '.yml']:
                data = yaml.safe_load(f)
            elif ext == '.json':
                data = json.load(f)
            else:
                raise ValueError("Wrong extension '%s' of file '%s'" % (ext, path))
            print("OK")
        return data


class RegisterMapReader(_Reader):
    """Read register map and configuration from JSON/YAML file.

    Examples:

        Read provided file and create :class:`RegisterMap` object:

        >>> reader = RegisterMapReader()
        >>> rmap = reader('../tests/data/map.json')
        Read '../tests/data/map.json' CSR map file with RegisterMapReader:
          Open file ... OK
          Read configuration ... OK
          Read registers ... OK

    """
    def __call__(self, path, config=Configuration()):
        """Read JSON/YAML file and fill RegisterMap object attributes.

        Returns:
            RegisterMap object.
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
        for json_reg in data['registers']:
            json_reg_filtered = {k: v for k, v in json_reg.items() if k in ['name', 'description', 'address']}
            reg = Register(**json_reg_filtered)
            for json_bf in json_reg['bit_fields']:
                reg.add_bfields(BitField(**json_bf))
            rmap.add_regs(reg)
        print("OK")
        return rmap


class ConfigurationReader(_Reader):
    """Read configuration from JSON/YAML file.

    Examples:

    """
    def __call__(self, path):
        """Read configuration from JSON/YAML file.

        Returns:
            Configuration object.
        """
        print("Read '%s' file with ConfigurationReader:" % path)
        data = self._open_file(path)
        print("  Read configuration ... ", end='')
        config = Configuration()
        config.values = data
        print("OK")
        return config
