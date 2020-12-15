#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Writers based on a CSR map internal representation (RegisterMap object).
"""

import json
import yaml


class JSONWriter():
    """Write CSR map description file to a JSON file.

    Examples:

        Create JSON file based on a :class:`RegisterMap` object:

        >>> writer = JSONWriter()
        >>> rmap = RegisterMap(config=Configuration())
        >>> writer('_build/doctest/map.json', rmap)
        Write '_build/doctest/map.json' file with JSONWriter:
          Prepare data ... OK
          Save data to file ... OK
    """
    def __init__(self):
        pass

    def __call__(self, path, rmap):
        """Write JSON file based on RegisterMap object attributes."""
        print("Write '%s' file with JSONWriter:" % path)
        print("  Prepare data ... ", end='')
        json_data = {
            'name': rmap.name,
            'version': rmap.version,
            'configuration': rmap.config.as_dict(),
            'register_map': list(rmap.as_dict().values())
        }
        print("OK")

        print("  Save data to file ... ", end='')
        with open(path, 'w') as json_file:
            json.dump(json_data, json_file, indent=4)
        print("OK")


class YAMLWriter():
    """Write CSR map description file to a YAML file.

    Examples:

        Create YAML file based on a :class:`RegisterMap` object:

        >>> writer = YAMLWriter()
        >>> rmap = RegisterMap(config=Configuration())
        >>> writer('_build/doctest/map.yaml', rmap)
        Write '_build/doctest/map.yaml' file with YAMLWriter:
          Prepare data ... OK
          Save data to file ... OK
    """
    def __init__(self):
        pass

    def __call__(self, path, rmap):
        """Write YAML file based on RegisterMap object attributes."""
        print("Write '%s' file with YAMLWriter:" % path)
        print("  Prepare data ... ", end='')
        yaml_data = {
            'name': rmap.name,
            'version': rmap.version,
            'configuration': rmap.config.as_dict(),
            'register_map': list(rmap.as_dict().values())
        }
        print("OK")

        print("  Save data to file ... ", end='')
        with open(path, 'w') as yaml_file:
            yaml.Dumper.ignore_aliases = lambda *args: True  # hack to disable aliases
            yaml.dump(yaml_data, yaml_file, default_flow_style=False, sort_keys=False)
        print("OK")
