#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Created with Corsair vgit-latest

Control/status register map.
"""


class _RegData:
    def __init__(self, rmap):
        self._rmap = rmap

    @property
    def val(self):
        """Value of the register"""
        rdata = self._rmap._if.read(self._rmap.DATA_ADDR)
        return (rdata >> self._rmap.DATA_VAL_POS) & self._rmap.DATA_VAL_MSK

    @val.setter
    def val(self, val):
        rdata = self._rmap._if.read(self._rmap.DATA_ADDR)
        rdata = rdata & (~(self._rmap.DATA_VAL_MSK << self._rmap.DATA_VAL_POS))
        rdata = rdata | (val << self._rmap.DATA_VAL_POS)
        self._rmap._if.write(self._rmap.DATA_ADDR, rdata)


class _RegCtrl:
    def __init__(self, rmap):
        self._rmap = rmap

    @property
    def val(self):
        """Value of the register"""
        rdata = self._rmap._if.read(self._rmap.CTRL_ADDR)
        return (rdata >> self._rmap.CTRL_VAL_POS) & self._rmap.CTRL_VAL_MSK

    @val.setter
    def val(self, val):
        rdata = self._rmap._if.read(self._rmap.CTRL_ADDR)
        rdata = rdata & (~(self._rmap.CTRL_VAL_MSK << self._rmap.CTRL_VAL_POS))
        rdata = rdata | (val << self._rmap.CTRL_VAL_POS)
        self._rmap._if.write(self._rmap.CTRL_ADDR, rdata)


class _RegStatus:
    def __init__(self, rmap):
        self._rmap = rmap

    @property
    def val(self):
        """Value of the register"""
        rdata = self._rmap._if.read(self._rmap.STATUS_ADDR)
        return (rdata >> self._rmap.STATUS_VAL_POS) & self._rmap.STATUS_VAL_MSK


class _RegStart:
    def __init__(self, rmap):
        self._rmap = rmap

    @property
    def val(self):
        """Value of the register"""
        return 0

    @val.setter
    def val(self, val):
        rdata = self._rmap._if.read(self._rmap.START_ADDR)
        rdata = rdata & (~(self._rmap.START_VAL_MSK << self._rmap.START_VAL_POS))
        rdata = rdata | (val << self._rmap.START_VAL_POS)
        self._rmap._if.write(self._rmap.START_ADDR, rdata)


class RegMap:
    """Control/Status register map"""

    # DATA - Data register
    DATA_ADDR = 0x0000
    DATA_VAL_POS = 0
    DATA_VAL_MSK = 0xffffffff

    # CTRL - Control register
    CTRL_ADDR = 0x0004
    CTRL_VAL_POS = 0
    CTRL_VAL_MSK = 0xffff

    # STATUS - Status register
    STATUS_ADDR = 0x0008
    STATUS_VAL_POS = 0
    STATUS_VAL_MSK = 0xff

    # START - Start register
    START_ADDR = 0x0100
    START_VAL_POS = 0
    START_VAL_MSK = 0x1

    def __init__(self, interface):
        self._if = interface

    @property
    def data(self):
        """Data register"""
        return self._if.read(self.DATA_ADDR)

    @data.setter
    def data(self, val):
        self._if.write(self.DATA_ADDR, val)

    @property
    def data_bf(self):
        return _RegData(self)

    @property
    def ctrl(self):
        """Control register"""
        return self._if.read(self.CTRL_ADDR)

    @ctrl.setter
    def ctrl(self, val):
        self._if.write(self.CTRL_ADDR, val)

    @property
    def ctrl_bf(self):
        return _RegCtrl(self)

    @property
    def status(self):
        """Status register"""
        return self._if.read(self.STATUS_ADDR)

    @property
    def status_bf(self):
        return _RegStatus(self)

    @property
    def start(self):
        """Start register"""
        return 0

    @start.setter
    def start(self, val):
        self._if.write(self.START_ADDR, val)

    @property
    def start_bf(self):
        return _RegStart(self)
