#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Writers based on a CSR map internal representation (RegisterMap object).
"""

import json
import yaml
import copy


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
            json.dump(json_data, json_file, indent=4)


class YAMLWriter():
    """Write CSR map description file to a YAML file."""
    def __init__(self):
        pass

    def __call__(self, path, rmap):
        """Write YAML file based on RegisterMap object attributes."""
        yaml_data = {
            'configuration': rmap.config.as_dict(),
            'register_map': list(rmap.as_dict().values())
        }
        with open(path, 'w') as yaml_file:
            yaml.Dumper.ignore_aliases = lambda *args: True  # hack to disable aliases
            yaml.dump(yaml_data, yaml_file, default_flow_style=False, sort_keys=False)
