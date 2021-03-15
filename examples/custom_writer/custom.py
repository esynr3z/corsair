#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Some custom processing based on corsair
"""
from corsair import RegisterMapReader, Jinja2Writer


# read register map description file
rmap = RegisterMapReader()('regmap.json')


# create custom writer, i.e. to write csv file
class CsvWriter(Jinja2Writer):
    def __call__(self, path, rmap):
        print("Write '%s' file with CsvWriter:" % path)
        j2_template = 'csv.j2'
        rmap._validate()

        j2_vars = {}
        j2_vars['rmap'] = rmap
        j2_vars['config'] = rmap.config

        self.render_to_file(j2_template, j2_vars, path, templates_path='.')


# generate CSV file from register map
CsvWriter()('rmap.csv', rmap)
