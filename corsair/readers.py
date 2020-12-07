#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""CSR map description file readers.
"""

import json
from .config import Configuration
from .regmap import BitField, Register, RegisterMap


class JSONReader():
    """Read CSR map description file in JSON format."""
    def __init__(self):
        pass

    def __call__(self, path):
        """Read JSON file and fill RegisterMap object attributes.

        Returns:
            RegisterMap object.
        """
        with open(path) as json_file:
            json_data = json.load(json_file)

            # Read configuration
            config = Configuration()
            config.values = json_data['configuration']

            # Read register map
            rmap = RegisterMap(config=config)
            for json_reg in json_data['register_map']:
                json_reg_filtered = {k: v for k, v in json_reg.items() if k in ['name', 'description', 'address']}
                reg = Register(**json_reg_filtered)
                for json_bf in json_reg['bit_fields']:
                    reg.add_bfields(BitField(**json_bf))
                rmap.add_regs(reg)

            return rmap
