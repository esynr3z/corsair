#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Demostration of Register API
"""

import copy
from corsair import BitField, Register, config

# create
csr_cnt = Register('CNT', 'Counter for some events', 0x10)

# access to the attributes
csr_cnt.address = 0
print("%s.address = 0x%x" % (csr_cnt.name, csr_cnt.address))

# add single bitfield
csr_cnt.add_bitfields(BitField('EVA', 'Some event A counter',
                               lsb=0, width=4, reset=0x000, access='rw', hardware='oie'))

# add several bitfields
csr_cnt.add_bitfields([
    BitField('EVB', 'Some event B counter',
             lsb=8, width=4, reset=0x000, access='rw', hardware='oie'),
    BitField('EVC', 'Some event C counter',
             lsb=16, width=4, reset=0x000, access='rw', hardware='oie')
])

# you can use chaining to create register and add bit fields in one action
csr_cnt = Register('CNT', 'Counter for some events', 0x10).add_bitfields([
    BitField('EVA', 'Some event A counter',
             lsb=0, width=4, reset=0x000, access='rw', hardware='oie'),
    BitField('EVB', 'Some event B counter',
             lsb=8, width=4, reset=0x000, access='rw', hardware='oie'),
    BitField('EVC', 'Some event C counter',
             lsb=16, width=4, reset=0x000, access='rw', hardware='oie')
])

# print name of the bitfields
print(csr_cnt.bitfield_names)

# check equality based on all the attributes (including bitields)
csr_lena = Register('LENA', 'Length of some pulse A', 0x0)
csr_lena.add_bitfields(BitField('VAL', 'CSR value', width=32, access='rw'))
assert csr_lena != csr_cnt
csr_cnt_clone = copy.deepcopy(csr_cnt)
assert csr_cnt == csr_cnt_clone

# print as string
print(repr(csr_cnt))
print("%s" % csr_cnt)

# conversions
print(csr_cnt.as_str())
print(csr_cnt.as_dict())

# count bitfields
print("number of bitfields: %d" % len(csr_cnt))

# iterate through bitfields
for i, bf in enumerate(csr_cnt):
    print("%d: %s" % (i, bf.name))

# access to the bitfield by name
print("EVB description: %s" % csr_cnt['EVB'].description)

# access to the bitfield by index (they are sorted in an ascending order of msb values)
print("EVB description: %s" % csr_cnt[1].description)

# validate the register and all it's bitfields
csr_cnt.validate()

# global configuration is important
globcfg = config.default_globcfg()
globcfg['data_width'] = 16
config.set_globcfg(globcfg)
try:
    rega = Register('REGA', 'Register A', 0x10)
    rega.add_bitfields(BitField('BFA', 'Bitfield A', lsb=0, width=32))
except AssertionError as e:
    print(e)

# add extra properties
reg = Register(the_answer=42)
assert reg.etc['the_answer'] == 42
