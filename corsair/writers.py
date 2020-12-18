#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Writers based on a CSR map internal representation (RegisterMap object).
"""

import os
import json
import yaml
import jinja2
from .__version__ import __version__
from pathlib import Path


class CsrJsonWriter():
    """Write CSR map description file to a JSON file.

    Examples:

        Create JSON file based on a :class:`RegisterMap` object:

        >>> writer = CsrJsonWriter()
        >>> rmap = RegisterMap(config=Configuration())
        >>> writer('_build/doctest/map.json', rmap)
        Write '_build/doctest/map.json' file with CsrJsonWriter:
          Prepare data ... OK
          Save data to file ... OK
    """
    def __init__(self):
        self.description = 'Write CSR map description file to a JSON file'

    def __call__(self, path, rmap):
        """Write JSON file based on RegisterMap object attributes."""
        print("Write '%s' file with CsrJsonWriter:" % path)
        print("  Prepare data ... ", end='')
        json_data = {
            'name': rmap.name,
            'version': rmap.version,
            'configuration': rmap.config.as_dict(),
            'registers': list(rmap.as_dict().values())
        }
        print("OK")

        print("  Save data to file ... ", end='')
        with open(path, 'w') as json_file:
            json.dump(json_data, json_file, indent=4)
        print("OK")


class CsrYamlWriter():
    """Write CSR map description file to a YAML file.

    Examples:

        Create YAML file based on a :class:`RegisterMap` object:

        >>> writer = CsrYamlWriter()
        >>> rmap = RegisterMap(config=Configuration())
        >>> writer('_build/doctest/map.yaml', rmap)
        Write '_build/doctest/map.yaml' file with CsrYamlWriter:
          Prepare data ... OK
          Save data to file ... OK
    """
    def __init__(self):
        self.description = 'Write CSR map description file to a YAML file'

    def __call__(self, path, rmap):
        """Write YAML file based on RegisterMap object attributes."""
        print("Write '%s' file with CsrYamlWriter:" % path)
        print("  Prepare data ... ", end='')
        yaml_data = {
            'name': rmap.name,
            'version': rmap.version,
            'configuration': rmap.config.as_dict(),
            'registers': list(rmap.as_dict().values())
        }
        print("OK")

        print("  Save data to file ... ", end='')
        with open(path, 'w') as yaml_file:
            yaml.Dumper.ignore_aliases = lambda *args: True  # hack to disable aliases
            yaml.dump(yaml_data, yaml_file, default_flow_style=False, sort_keys=False)
        print("OK")


class _Jinja2Writer():
    """Basic class for Jinja2-based writers."""

    def _render_to_file(self, template, vars, path):
        """Render text with Jinja2 and save it to file

        Args:
            template : path to Jinja2 template
            vars : dictionary with template variables
            path : path to output file
        """
        print("  Load template ... ", end='')
        templates_path = str(Path(__file__).parent / 'templates')
        j2_env = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath=templates_path))
        j2_template = j2_env.get_template(template)
        print("OK")

        print("  Render text ... ", end='')
        rendered_text = j2_template.render(vars)
        print("OK")

        print("  Save data to file ... ", end='')
        with open(path, "w") as f:
            f.write(rendered_text)
        print("OK")


class BridgeVerilogWriter(_Jinja2Writer):
    """Create Verilog file with bridge to Local Bus.

    Examples:

        Create Verilog file with APB to Local Bus bridge:

        >>> rmap = RegisterMap(config=Configuration())
        >>> rmap.config['interface_generic']['type'].value = 'apb'
        >>> writer = BridgeVerilogWriter()
        >>> writer('_build/doctest/lb_bridge.v', rmap)
        Write '_build/doctest/lb_bridge.v' file with BridgeVerilogWriter:
          Prepare data ... OK
          Load template ... OK
          Render text ... OK
          Save data to file ... OK
    """
    def __init__(self):
        self.description = 'Create bridge to Local Bus module in Verilog.'

    def __call__(self, path, rmap):
        """Create bridge to Local Bus in Verilog."""

        intf_config = rmap.config['interface_generic']
        intf_config.add_params(rmap.config['interface_specific'].params)
        if intf_config['type'].value == 'axil':
            j2_template = 'axil2lb_verilog.j2'
        elif intf_config['type'].value == 'apb':
            j2_template = 'apb2lb_verilog.j2'
        elif intf_config['type'].value == 'amm':
            j2_template = 'amm2lb_verilog.j2'
        else:
            print("Local Bus is selected for the CSR interface. Bridge will not be generated.")
            return

        print("Write '%s' file with BridgeVerilogWriter:" % path)
        print("  Prepare data ... ", end='')

        j2_vars = {}

        j2_vars['corsair_ver'] = __version__
        j2_vars['csr_ver'] = rmap.version
        j2_vars['csr_name'] = rmap.name
        j2_vars['module_name'] = Path(path).stem
        j2_vars['config'] = intf_config

        print("OK")

        self._render_to_file(j2_template, j2_vars, path)
