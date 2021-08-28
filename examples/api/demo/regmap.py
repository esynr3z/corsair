#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Create register map and generate outputs with Corsair library
"""
from corsair import BitField, Register, RegisterMap, EnumValue, generators, config

# global configuration
globcfg = config.default_globcfg()
globcfg['data_width'] = 32
globcfg['address_width'] = 16
globcfg['register_reset'] = 'async_neg'
# make sure you've aplied global configuration before doing anything else
config.set_globcfg(globcfg)

# register map
rmap = RegisterMap()

rmap.add_registers(Register('DATA', 'Data register', 0x0).add_bitfields([
    BitField("FIFO", "Write to push value to TX FIFO, read to get data from RX FIFO",
             width=8, lsb=0, access='rw', hardware='q'),
    BitField("FERR", "Frame error flag. Read to clear.", width=1, lsb=16, access='rolh', hardware='i'),
    BitField("PERR", "Parity error flag. Read to clear.", width=1, lsb=17, access='rolh', hardware='i'),
]))

rmap.add_registers(Register('STAT', 'Status register', 0x4).add_bitfields([
    BitField("BUSY", "Transciever is busy", width=1, lsb=0, access='ro', hardware='ie'),
    BitField("RXE", "RX FIFO is empty", width=1, lsb=4, access='ro', hardware='i'),
    BitField("TXF", "TX FIFO is full", width=1, lsb=5, access='ro', hardware='i'),
]))

rmap.add_registers(Register('CTRL', 'Control register', 0x8).add_bitfields([
    BitField("BAUD", "Baudrate value", width=2, lsb=0, access='rw', hardware='o').add_enums([
        EnumValue("B9600", 0, "9600 baud"),
        EnumValue("B38400", 1, "38400 baud"),
        EnumValue("B115200", 2, "115200 baud"),
    ]),
    BitField("TXEN", "Transmitter enable. Can be disabled by hardware on error.",
             width=1, lsb=4, access='rw', hardware='oie'),
    BitField("RXEN", "Receiver enable. Can be disabled by hardware on error.",
             width=1, lsb=5, access='rw', hardware='oie'),
    BitField("TXST", "Force transmission start", width=1, lsb=6, access='wosc', hardware='o'),
]))

rmap.add_registers(Register('LPMODE', 'Low power mode control', 0xC).add_bitfields([
    BitField("DIV", "Clock divider in low power mode", width=8, lsb=0, access='rw', hardware='o'),
    BitField("EN", "Low power mode enable", width=1, lsb=31, access='rw', hardware='o'),
]))

rmap.add_registers(Register('INTSTAT', 'Interrupt status register', 0x10).add_bitfields([
    BitField("TX", "Transmitter interrupt flag. Write 1 to clear.", width=1, lsb=0, access='rw1c', hardware='s'),
    BitField("RX", "Receiver interrupt. Write 1 to clear.", width=1, lsb=1, access='rw1c', hardware='s'),
]))

rmap.add_registers(Register('ID', 'IP-core ID register', 0xFFC).add_bitfields([
    BitField("UID", "Unique ID", width=32, lsb=0, access='ro', hardware='f', reset=0xcafe0666),
]))

# outputs
generators.Verilog(rmap, 'regs.v', interface='apb').generate()
generators.Markdown(rmap, 'regs.md', print_images=False).generate()
