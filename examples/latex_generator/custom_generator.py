#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Create custom LaTeX generator
"""
from corsair import RegisterMap, Register, BitField, generators, config, utils, __version__
import yaml

class TexGenerator(generators.Generator, generators.Jinja2):
    """Create TeX file in HIL camera adapter style.

    :param rmap: Register map object
    :type rmap: :class:`corsair.RegisterMap`
    :param path: Path to the output file
    :type path: str
    """
    
    def __init__(self, rmap=None, path='regs.tex', **args):
        super().__init__(rmap, **args)
        self.path = path

    def create_res_bitfield(self, lsb, width):
        bf_res = BitField(name=f'RES{lsb}', description='Reserved', width=width, lsb=lsb, access='ro')
        return bf_res

    def fill_reg_gaps(self, register, register_width):
        reg_new = Register("temp")
        next_lsb = 0
        for bf in register['bitfields']:
            if bf['lsb'] > next_lsb:
                bf_new = self.create_res_bitfield(next_lsb, bf['lsb'] - next_lsb)
                reg_new.add_bitfields(bf_new)
            next_lsb = bf['lsb'] + bf['width']
        if next_lsb < register_width:
            bf_new = self.create_res_bitfield(next_lsb, register_width - next_lsb)
            reg_new.add_bitfields(bf_new)
        return reg_new
    
    def read_yaml(self, path):
        """Read register map from YAML file."""
        with open(path, 'r') as f:
            return yaml.safe_load(f)

    def generate(self):
        # validate parameters
        self.validate()

        # Fill gaps in registers
        for reg in self.rmap.regs:
            gap_bfs = self.fill_reg_gaps(reg.as_dict(), config.globcfg['data_width'])
            reg.add_bitfields(gap_bfs.bitfields)

        # revalidate parameters
        print("... validate updated register map")
        self.validate()

        # prepare jinja2
        j2_template = 'regs_tex.j2'
        j2_vars = {}
        j2_vars['rmap'] = self.rmap 
        j2_vars['config'] = config.globcfg
        # render
        self.render_to_file(j2_template, j2_vars, self.path, ".")



""" Create custom VHDL generator
"""
class SxVhdlGenerator(generators.Generator, generators.Jinja2):
    """Create VHDL file in SX style with register map.

    :param rmap: Register map object
    :type rmap: :class:`corsair.RegisterMap`
    :param path: Path to the output file
    :type path: str
    :param read_filler: Numeric value to return if wrong address was read
    :type read_filler: int
    """
    import datetime
    import os

    def __init__(self, rmap=None, path='regs.vhd', project='N/A', read_filler=0, **args):
        super().__init__(rmap, **args)
        self.path = path
        self.project = project
        self.read_filler = read_filler

    def generate(self):
        # validate parameters
        self.validate()
        # prepare jinja2
        j2_template = 'regmap_sx_vhdl.j2'
        j2_vars = {}
        j2_vars['corsair_ver'] = __version__
        j2_vars['rmap'] = self.rmap
        j2_vars['date'] = self.datetime.datetime.now().strftime("%d.%m.%Y")
        j2_vars['author'] = self.os.getlogin()
        j2_vars['module_name'] = utils.get_file_name(self.path)
        j2_vars['read_filler'] = utils.str2int(self.read_filler)
        j2_vars['config'] = config.globcfg
        # render
        self.render_to_file(j2_template, j2_vars, self.path, ".")