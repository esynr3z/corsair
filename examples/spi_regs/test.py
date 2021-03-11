#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Test of an access to FPGA register map
"""

from time import sleep
from drv_rmap import ftdi_show_devices, FtdiSpi, Fpga
from rmap import RegMap

# first of all, check if FTDI devices is available and get an URL
ftdi_show_devices()

# create FPGA object with register map and interface to access it
# FTDI URL is obtained from ftdi_show_devices() output
# cs is 1, because ADBUS4 is used for the CSn signal
spi = FtdiSpi(ftdi_url='ftdi://ftdi:2232:1:12/1', cs=1, spi_freq=1e6)
rmap = RegMap(spi)
fpga = Fpga(rmap)

# direct spi transactions
# read address 0x00 (LEDCTRL)
print('address 0x0: 0x%04x' % fpga.spi.read(0x0))
# read address 0x83 (no register here)
print('address 0x83: 0x%04x' % fpga.spi.read(0x83))
# turn on all leds
fpga.spi.write(0x0, 0xffff)
sleep(1)
# turn off all leds
fpga.spi.write(0x0, 0x0000)
sleep(1)
print('---')

# control leds through regmap: single write style (access to the register)
# turn on RED
fpga.rmap.ledctrl = 1 << fpga.rmap.LEDCTRL_REN_POS  # SPI write under the hood
print('ledctrl: 0x%04x' % fpga.rmap.ledctrl)  # SPI read under the hood
sleep(1)
# turn off RED, turn on GREEN
fpga.rmap.ledctrl = 1 << fpga.rmap.LEDCTRL_GEN_POS
print('ledctrl: 0x%04x' % fpga.rmap.ledctrl)
sleep(1)
# turn off GREEN, turn on BLUE
fpga.rmap.ledctrl = 1 << fpga.rmap.LEDCTRL_BEN_POS
print('ledctrl: 0x%04x' % fpga.rmap.ledctrl)
sleep(1)
# turn off BLUE
fpga.rmap.ledctrl = 0
print('ledctrl: 0x%04x' % fpga.rmap.ledctrl)
sleep(1)
print('---')

# control leds through regmap: read-modify-write style (access to the bitfields)
# turn on RED
fpga.rmap.ledctrl_bf.ren = 1  # SPI read, modify, SPI write
print('ledctrl.ren: 0x%01x' % fpga.rmap.ledctrl_bf.ren)  # SPI read, mask and shift result
print('ledctrl: 0x%04x' % fpga.rmap.ledctrl)  # SPI read
sleep(1)
# turn on GREEN (yellow)
fpga.rmap.ledctrl_bf.gen = 1
print('ledctrl.gen: 0x%01x' % fpga.rmap.ledctrl_bf.gen)
print('ledctrl: 0x%04x' % fpga.rmap.ledctrl)
sleep(1)
# turn on BLUE (white)
fpga.rmap.ledctrl_bf.ben = 1
print('ledctrl.gen: 0x%01x' % fpga.rmap.ledctrl_bf.ben)
print('ledctrl: 0x%04x' % fpga.rmap.ledctrl)
sleep(1)
# turn of all
fpga.rmap.ledctrl = 0
print('ledctrl: 0x%04x' % fpga.rmap.ledctrl)
sleep(1)

fpga.disconnect()
