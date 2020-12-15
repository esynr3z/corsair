#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""CSR map description file readers.
"""

import json
import yaml
from .config import Configuration
from .regmap import BitField, Register, RegisterMap


class JSONReader():
    """Read CSR map description file in JSON format.

    Examples:

        Read provided file and create :class:`RegisterMap` object:

        >>> reader = JSONReader()
        >>> rmap = reader('../tests/data/map.json')
        Read '../tests/data/map.json' CSR map file with JSONReader:
          Open file ... OK
          Read configuration ... OK
          Read register map ... OK

    """
    def __init__(self):
        pass

    def __call__(self, path):
        """Read JSON file and fill RegisterMap object attributes.

        Returns:
            RegisterMap object.
        """
        print("Read '%s' CSR map file with JSONReader:" % path)
        with open(path, 'r') as json_file:
            print("  Open file ... ", end='')
            json_data = json.load(json_file)
            print("OK")

            # Read configuration
            print("  Read configuration ... ", end='')
            config = Configuration()
            config.values = json_data['configuration']
            print("OK")

            # Read register map
            print("  Read register map ... ", end='')
            rmap_name = json_data['name']
            rmap_version = json_data['version']
            rmap = RegisterMap(config=config, name=rmap_name, version=rmap_version)
            for json_reg in json_data['register_map']:
                json_reg_filtered = {k: v for k, v in json_reg.items() if k in ['name', 'description', 'address']}
                reg = Register(**json_reg_filtered)
                for json_bf in json_reg['bit_fields']:
                    reg.add_bfields(BitField(**json_bf))
                rmap.add_regs(reg)
            print("OK")

            return rmap


class YAMLReader():
    """Read CSR map description file in YAML format.

    Examples:

        Read provided file and create :class:`RegisterMap` object:

        >>> reader = YAMLReader()
        >>> rmap = reader('../tests/data/map.yml')
        Read '../tests/data/map.yml' CSR map file with YAMLReader:
          Open file ... OK
          Read configuration ... OK
          Read register map ... OK
    """
    def __init__(self):
        pass

    def __call__(self, path):
        """Read YAML file and fill RegisterMap object attributes.

        Returns:
            RegisterMap object.
        """
        print("Read '%s' CSR map file with YAMLReader:" % path)
        with open(path, 'r') as yaml_file:
            print("  Open file ... ", end='')
            yaml_data = yaml.safe_load(yaml_file)
            print("OK")

            # Read configuration
            print("  Read configuration ... ", end='')
            config = Configuration()
            config.values = yaml_data['configuration']
            print("OK")

            # Read register map
            print("  Read register map ... ", end='')
            rmap_name = yaml_data['name']
            rmap_version = yaml_data['version']
            rmap = RegisterMap(config=config, name=rmap_name, version=rmap_version)
            for yaml_reg in yaml_data['register_map']:
                yaml_reg_filtered = {k: v for k, v in yaml_reg.items() if k in ['name', 'description', 'address']}
                reg = Register(**yaml_reg_filtered)
                for yaml_bf in yaml_reg['bit_fields']:
                    reg.add_bfields(BitField(**yaml_bf))
                rmap.add_regs(reg)
            print("OK")

            return rmap
