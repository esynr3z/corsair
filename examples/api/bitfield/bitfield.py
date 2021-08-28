#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Demostration of Bitfield API
"""

import copy
from corsair import BitField, EnumValue

# create bitfield
bf_cnt = BitField('CNT', 'Counter value', lsb=8, width=32, reset=0xFFFF, access='rw', hardware='o')
# and check if it correct
bf_cnt.validate()

# access to the attributes
bf_cnt.width = 16
print("%s.msb = %d" % (bf_cnt.name, bf_cnt.msb))

# check equality based on all the attributes
bf_data = BitField('DATA', 'Data value', lsb=8, width=32, reset=0xFFFF, access='rw', hardware='o')
assert bf_data != bf_cnt
bf_cnt_clone = copy.deepcopy(bf_cnt)
assert bf_cnt == bf_cnt_clone

# print as string
print(repr(bf_cnt))
print("%s" % bf_cnt)

# conversions
print(bf_cnt.as_str())
print(bf_cnt.as_dict())

# add single enum value
bf_ctrl = BitField('MODE', 'Current mode', lsb=8, width=4, reset=0, access='rw', hardware='o')
bf_ctrl.add_enums(EnumValue('IDLE', 0, 'IDLE mode'))

# add several enums
bf_ctrl.add_enums([EnumValue('STOP', 2, 'Stop mode'), EnumValue('ACTIVE', 3, 'Active mode')])

# you can use chaining to create bit field and add enums in one action
bf_ctrl = BitField('MODE', 'Current mode', lsb=8, width=4, reset=0, access='rw', hardware='o').add_enums([
    EnumValue('IDLE', 0, 'IDLE mode'),
    EnumValue('STOP', 2, 'Stop mode'),
    EnumValue('ACTIVE', 3, 'Active mode')
])

# print name of the enums
print(bf_ctrl.enum_names)

# count enum values
print("number of enums: %d" % len(bf_ctrl))

# iterate through enums
for i, enum in enumerate(bf_ctrl):
    print("%d: %s" % (i, enum.name))

# access to the enum by name
print("IDLE description: %s" % bf_ctrl['IDLE'].description)

# access to the enum by index (they are sorted in an ascending order of values)
print("STOP description: %s" % bf_ctrl[1].description)

# add extra attributes to bitfield
bf = BitField(the_answer=42)
assert bf.etc['the_answer'] == 42
