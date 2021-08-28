#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Demostration of RegisterMap API
"""

import copy
from corsair import BitField, Register, RegisterMap

# create
# register map
rmap = RegisterMap()

# add single registers
csr_lena = Register('LENA', 'Length of some pulse A', 0x0).add_bitfields(
    BitField('VAL', 'CSR value', width=32, access='rw', hardware='o'))
rmap.add_registers(csr_lena)

# add several registers
rmap.add_registers([
    Register('LENB', 'Length of some pulse B', 0x4).add_bitfields(
        BitField('VAL', 'CSR value', lsb=8, width=16, reset=0xFFFF, access='rw', hardware='o')),
    Register('FIFORO', 'Read only FIFO', 0x64).add_bitfields(
        BitField('DATA', 'Data', lsb=0, width=24, access='ro', hardware='i'))
])

# print name of the registers
print(rmap.reg_names)

# check equality based on all the attributes
rmap_clone = copy.deepcopy(rmap)
assert rmap_clone == rmap
rmap_clone['LENA'].address = 0x8
assert rmap_clone != rmap

# print as string
print(repr(rmap))
print("%s" % rmap)

# conversions
print(rmap.as_str())
print(rmap.as_dict())

# count registers
print("number of registers: %d" % len(rmap))

# iterate through registers
for i, reg in enumerate(rmap):
    print("%d: %s" % (i, reg.name))

# access to the register by name
print("LENA description: %s" % rmap['LENA'].description)

# access to the register by index (they are sorted in an ascending order of address values)
print("LENA description: %s" % rmap[0].description)

# validate all the components of the register map recursevely
rmap.validate()
