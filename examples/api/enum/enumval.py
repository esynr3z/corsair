#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Demostration of EnumValue API
"""

import copy
from corsair import EnumValue

# create enum
enum_a = EnumValue('A', 1, 'A description')
# and check if it correct
enum_a.validate()

# access to the attributes
enum_a.value = 0
print("%s.value = %d" % (enum_a.name, enum_a.value))

# check equality based on all the attributes
enum_b = EnumValue('B', 2, 'B description')
assert enum_a != enum_b
enum_a_clone = copy.deepcopy(enum_a)
assert enum_a == enum_a_clone

# add extra properties
enum_c = EnumValue('C', 0, 'C description', the_answer=42)
assert enum_c.etc['the_answer'] == 42

# print as string
print(repr(enum_a))
print("%s" % enum_a)

# conversions
print(enum_a.as_str())
print(enum_a.as_dict())
