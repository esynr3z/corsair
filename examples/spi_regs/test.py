#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Test of an access to FPGA register map
"""

from time import sleep
from drv_rmap import ftdi_show_devices, FtdiSpi, Fpga
from rmap import RegMap

# First of all, uncomment this and check if FTDI devices is available.
# You will also need an URL later.
# ftdi_show_devices()
# exit()

# create FPGA object with register map and interface to access it
spi = FtdiSpi(ftdi_url='ftdi://ftdi:2232:1:12/1', cs=1, spi_freq=1e6)
rmap = RegMap(spi)
fpga = Fpga(rmap)

print('0x%04x' % fpga.spi.read(0x81))
print('0x%04x' % fpga.rmap.ledctrl)
print('0x%04x' % fpga.spi.read(0x83))
print('----')
print('0x%04x' % fpga.rmap.rdfifo)
print('0x%04x' % fpga.rmap.rdfifo)
print('0x%04x' % fpga.rmap.rdfifo)
print('0x%04x' % fpga.rmap.rdfifo)

fpga.rmap.ledctrl = 0xffff
sleep(1)
fpga.rmap.ledctrl = 0x3
sleep(1)
fpga.rmap.ledctrl = 0x4
sleep(1)

fpga.disconnect()
