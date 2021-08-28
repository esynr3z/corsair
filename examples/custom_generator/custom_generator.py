#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Create custom generator
"""
from corsair import RegisterMap, generators


class CsvGenerator(generators.Generator, generators.Jinja2):
    def __init__(self, rmap=None, path='regs.csv', custom_param=7, **args):
        super().__init__(rmap, **args)
        self.path = path
        self.custom_param = custom_param

    def generate(self):
        # validate parameters
        self.validate()
        # prepare jinja2
        j2_template = 'regs_csv.j2'
        j2_vars = {}
        j2_vars['rmap'] = self.rmap
        j2_vars['custom_param'] = self.custom_param
        # render
        self.render_to_file(j2_template, j2_vars, self.path, ".")
