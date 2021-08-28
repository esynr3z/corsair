#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Demostration of config API
"""

from corsair import config, generators

# read csrconfig
globcfg, targets = config.read_csrconfig("csrconfig")
config.validate_globcfg(globcfg)
print(globcfg)
print(targets)

# add targets
targets.update(generators.VerilogHeader(path="regs.vh").make_target('v_header'))

# apply configuration globally
globcfg['the_answer'] = 58
config.set_globcfg(globcfg)

# write it to the file
config.write_csrconfig("new.csrconfig", globcfg, targets)
