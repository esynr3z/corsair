#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Utility functions and classes
"""

from . import generators
import os
from . import config
from .reg import Register
from .enum import EnumValue
from .bitfield import BitField
from .regmap import RegisterMap
from pathlib import Path


def str2int(val, base=None):
    """String to integer conversion"""
    try:
        if isinstance(val, int) or val is None:
            return val
        elif base:
            return int(val, base)
        elif '0x' in val:
            return int(val, 16)
        elif '0b' in val:
            return int(val, 2)
        else:
            return int(val)
    except (ValueError, TypeError) as e:
        raise ValueError("Can't convert '%s' to int!" % val)


def str2bool(val):
    """String to integer conversion"""
    try:
        if isinstance(val, bool):
            return val
        elif not isinstance(val, str):
            return bool(val)
        elif val.lower() in ["true", "t", "yes", "y"]:
            return True
        elif val.lower() in ["false", "f", "no", "n"]:
            return False
        else:
            raise ValueError
    except (ValueError, AttributeError, TypeError) as e:
        raise ValueError("Can't convert '%s' to bool!" % val)


def int2str(val, max_dec=1024):
    """Make string from int. Hexademical representaion will be used if input value greater that 'max_dec'."""
    if val > max_dec:
        return "0x%x" % val
    else:
        return "%d" % val


def is_non_neg_int(val):
    """Check if value is non negative integer"""
    return isinstance(val, int) and val >= 0


def is_pos_int(val):
    """Check if value is positive integer"""
    return isinstance(val, int) and val > 0


def is_str(val):
    """Check if value is string"""
    return isinstance(val, str)


def is_list(val):
    """Check if value is list"""
    return isinstance(val, list)


def is_first_letter(val):
    """Check if string starts from a letter"""
    return ord(val[0].lower()) in range(ord('a'), ord('z') + 1)


def listify(obj):
    """Make lists from single objects. No changes are made for the argument of the 'list' type."""
    if is_list(obj):
        return obj
    else:
        return [obj]


def get_file_ext(path):
    _, ext = os.path.splitext(path)
    return ext.lower()


def get_file_name(path):
    return Path(path).stem


def create_dirs(path):
    dirs = Path(path).parent
    Path(dirs).mkdir(parents=True, exist_ok=True)


def force_name_case(name):
    if config.globcfg["force_name_case"] == "upper":
        return name.upper()
    elif config.globcfg["force_name_case"] == "lower":
        return name.lower()
    else:
        return name


def create_template_simple():
    """Generate simple register map template"""
    rmap = RegisterMap()

    rmap.add_registers(Register('DATA', 'Data register', 0x0).add_bitfields(
        BitField(width=32, access='rw', hardware='ioe')))

    rmap.add_registers(Register('CTRL', 'Control register', 0x4).add_bitfields(
        BitField(width=16, access='rw', reset=0x0100, hardware='o')))

    rmap.add_registers(Register('STATUS', 'Status register', 0x8).add_bitfields(
        BitField(width=8, access='ro', hardware='i')))

    rmap.add_registers(Register('START', 'Start register', 0x100).add_bitfields(
        BitField(width=1, access='wosc', hardware='o')))

    return rmap


def create_template():
    """Generate register map template"""
    # register map
    rmap = RegisterMap()

    rmap.add_registers(Register('DATA', 'Data register', 0x4).add_bitfields([
        BitField("FIFO", "Write to push value to TX FIFO, read to get data from RX FIFO",
                 width=8, lsb=0, access='rw', hardware='q'),
        BitField("FERR", "Frame error flag. Read to clear.", width=1, lsb=16, access='rolh', hardware='i'),
        BitField("PERR", "Parity error flag. Read to clear.", width=1, lsb=17, access='rolh', hardware='i'),
    ]))

    rmap.add_registers(Register('STAT', 'Status register', 0xC).add_bitfields([
        BitField("BUSY", "Transciever is busy", width=1, lsb=2, access='ro', hardware='ie'),
        BitField("RXE", "RX FIFO is empty", width=1, lsb=4, access='ro', hardware='i'),
        BitField("TXF", "TX FIFO is full", width=1, lsb=8, access='ro', hardware='i'),
    ]))

    rmap.add_registers(Register('CTRL', 'Control register', 0x10).add_bitfields([
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

    rmap.add_registers(Register('LPMODE', 'Low power mode control', 0x14).add_bitfields([
        BitField("DIV", "Clock divider in low power mode", width=8, lsb=0, access='rw', hardware='o'),
        BitField("EN", "Low power mode enable", width=1, lsb=31, access='rw', hardware='o'),
    ]))

    rmap.add_registers(Register('INTSTAT', 'Interrupt status register', 0x20).add_bitfields([
        BitField("TX", "Transmitter interrupt flag. Write 1 to clear.", width=1, lsb=0, access='rw1c', hardware='s'),
        BitField("RX", "Receiver interrupt. Write 1 to clear.", width=1, lsb=1, access='rw1c', hardware='s'),
    ]))

    rmap.add_registers(Register('ID', 'IP-core ID register', 0x40).add_bitfields([
        BitField("UID", "Unique ID", width=32, lsb=0, access='ro', hardware='f', reset=0xcafe0666),
    ]))

    return rmap
