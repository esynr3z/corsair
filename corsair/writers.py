#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Writers based on a CSR map internal representation (RegisterMap object).
"""

import json


class JSONWriter():
    """Write CSR map description file to a JSON file."""
    def __init__(self):
        pass

    def __call__(self, path, rmap):
        """Write JSON file based on RegisterMap object attributes."""
        json_data = {
            'configuration': rmap.config.as_dict(),
            'register_map': list(rmap.as_dict().values())
        }
        with open(path, 'w') as json_file:
            json_data = json.dump(json_data, json_file, indent=4)
