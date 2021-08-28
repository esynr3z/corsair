#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Created with Corsair vgit-latest

Control/status register map.
"""


class _RegData:
    def __init__(self, rmap):
        self._rmap = rmap

    @property
    def fifo(self):
        """Write to push value to TX FIFO, read to get data from RX FIFO"""
        rdata = self._rmap._if.read(self._rmap.DATA_ADDR)
        return (rdata >> self._rmap.DATA_FIFO_POS) & self._rmap.DATA_FIFO_MSK

    @fifo.setter
    def fifo(self, val):
        rdata = self._rmap._if.read(self._rmap.DATA_ADDR)
        rdata = rdata & (~(self._rmap.DATA_FIFO_MSK << self._rmap.DATA_FIFO_POS))
        rdata = rdata | (val << self._rmap.DATA_FIFO_POS)
        self._rmap._if.write(self._rmap.DATA_ADDR, rdata)

    @property
    def ferr(self):
        """Frame error flag. Read to clear."""
        rdata = self._rmap._if.read(self._rmap.DATA_ADDR)
        return (rdata >> self._rmap.DATA_FERR_POS) & self._rmap.DATA_FERR_MSK

    @property
    def perr(self):
        """Parity error flag. Read to clear."""
        rdata = self._rmap._if.read(self._rmap.DATA_ADDR)
        return (rdata >> self._rmap.DATA_PERR_POS) & self._rmap.DATA_PERR_MSK


class _RegStat:
    def __init__(self, rmap):
        self._rmap = rmap

    @property
    def busy(self):
        """Transciever is busy"""
        rdata = self._rmap._if.read(self._rmap.STAT_ADDR)
        return (rdata >> self._rmap.STAT_BUSY_POS) & self._rmap.STAT_BUSY_MSK

    @property
    def rxe(self):
        """RX FIFO is empty"""
        rdata = self._rmap._if.read(self._rmap.STAT_ADDR)
        return (rdata >> self._rmap.STAT_RXE_POS) & self._rmap.STAT_RXE_MSK

    @property
    def txf(self):
        """TX FIFO is full"""
        rdata = self._rmap._if.read(self._rmap.STAT_ADDR)
        return (rdata >> self._rmap.STAT_TXF_POS) & self._rmap.STAT_TXF_MSK


class _RegCtrl:
    def __init__(self, rmap):
        self._rmap = rmap

    @property
    def baud(self):
        """Baudrate value"""
        rdata = self._rmap._if.read(self._rmap.CTRL_ADDR)
        return (rdata >> self._rmap.CTRL_BAUD_POS) & self._rmap.CTRL_BAUD_MSK

    @baud.setter
    def baud(self, val):
        rdata = self._rmap._if.read(self._rmap.CTRL_ADDR)
        rdata = rdata & (~(self._rmap.CTRL_BAUD_MSK << self._rmap.CTRL_BAUD_POS))
        rdata = rdata | (val << self._rmap.CTRL_BAUD_POS)
        self._rmap._if.write(self._rmap.CTRL_ADDR, rdata)

    @property
    def txen(self):
        """Transmitter enable. Can be disabled by hardware on error."""
        rdata = self._rmap._if.read(self._rmap.CTRL_ADDR)
        return (rdata >> self._rmap.CTRL_TXEN_POS) & self._rmap.CTRL_TXEN_MSK

    @txen.setter
    def txen(self, val):
        rdata = self._rmap._if.read(self._rmap.CTRL_ADDR)
        rdata = rdata & (~(self._rmap.CTRL_TXEN_MSK << self._rmap.CTRL_TXEN_POS))
        rdata = rdata | (val << self._rmap.CTRL_TXEN_POS)
        self._rmap._if.write(self._rmap.CTRL_ADDR, rdata)

    @property
    def rxen(self):
        """Receiver enable. Can be disabled by hardware on error."""
        rdata = self._rmap._if.read(self._rmap.CTRL_ADDR)
        return (rdata >> self._rmap.CTRL_RXEN_POS) & self._rmap.CTRL_RXEN_MSK

    @rxen.setter
    def rxen(self, val):
        rdata = self._rmap._if.read(self._rmap.CTRL_ADDR)
        rdata = rdata & (~(self._rmap.CTRL_RXEN_MSK << self._rmap.CTRL_RXEN_POS))
        rdata = rdata | (val << self._rmap.CTRL_RXEN_POS)
        self._rmap._if.write(self._rmap.CTRL_ADDR, rdata)

    @property
    def txst(self):
        """Force transmission start"""
        return 0

    @txst.setter
    def txst(self, val):
        rdata = self._rmap._if.read(self._rmap.CTRL_ADDR)
        rdata = rdata & (~(self._rmap.CTRL_TXST_MSK << self._rmap.CTRL_TXST_POS))
        rdata = rdata | (val << self._rmap.CTRL_TXST_POS)
        self._rmap._if.write(self._rmap.CTRL_ADDR, rdata)


class _RegLpmode:
    def __init__(self, rmap):
        self._rmap = rmap

    @property
    def div(self):
        """Clock divider in low power mode"""
        rdata = self._rmap._if.read(self._rmap.LPMODE_ADDR)
        return (rdata >> self._rmap.LPMODE_DIV_POS) & self._rmap.LPMODE_DIV_MSK

    @div.setter
    def div(self, val):
        rdata = self._rmap._if.read(self._rmap.LPMODE_ADDR)
        rdata = rdata & (~(self._rmap.LPMODE_DIV_MSK << self._rmap.LPMODE_DIV_POS))
        rdata = rdata | (val << self._rmap.LPMODE_DIV_POS)
        self._rmap._if.write(self._rmap.LPMODE_ADDR, rdata)

    @property
    def en(self):
        """Low power mode enable"""
        rdata = self._rmap._if.read(self._rmap.LPMODE_ADDR)
        return (rdata >> self._rmap.LPMODE_EN_POS) & self._rmap.LPMODE_EN_MSK

    @en.setter
    def en(self, val):
        rdata = self._rmap._if.read(self._rmap.LPMODE_ADDR)
        rdata = rdata & (~(self._rmap.LPMODE_EN_MSK << self._rmap.LPMODE_EN_POS))
        rdata = rdata | (val << self._rmap.LPMODE_EN_POS)
        self._rmap._if.write(self._rmap.LPMODE_ADDR, rdata)


class _RegIntstat:
    def __init__(self, rmap):
        self._rmap = rmap

    @property
    def tx(self):
        """Transmitter interrupt flag. Write 1 to clear."""
        rdata = self._rmap._if.read(self._rmap.INTSTAT_ADDR)
        return (rdata >> self._rmap.INTSTAT_TX_POS) & self._rmap.INTSTAT_TX_MSK

    @tx.setter
    def tx(self, val):
        rdata = self._rmap._if.read(self._rmap.INTSTAT_ADDR)
        rdata = rdata & (~(self._rmap.INTSTAT_TX_MSK << self._rmap.INTSTAT_TX_POS))
        rdata = rdata | (val << self._rmap.INTSTAT_TX_POS)
        self._rmap._if.write(self._rmap.INTSTAT_ADDR, rdata)

    @property
    def rx(self):
        """Receiver interrupt. Write 1 to clear."""
        rdata = self._rmap._if.read(self._rmap.INTSTAT_ADDR)
        return (rdata >> self._rmap.INTSTAT_RX_POS) & self._rmap.INTSTAT_RX_MSK

    @rx.setter
    def rx(self, val):
        rdata = self._rmap._if.read(self._rmap.INTSTAT_ADDR)
        rdata = rdata & (~(self._rmap.INTSTAT_RX_MSK << self._rmap.INTSTAT_RX_POS))
        rdata = rdata | (val << self._rmap.INTSTAT_RX_POS)
        self._rmap._if.write(self._rmap.INTSTAT_ADDR, rdata)


class _RegId:
    def __init__(self, rmap):
        self._rmap = rmap

    @property
    def uid(self):
        """Unique ID"""
        rdata = self._rmap._if.read(self._rmap.ID_ADDR)
        return (rdata >> self._rmap.ID_UID_POS) & self._rmap.ID_UID_MSK


class RegMap:
    """Control/Status register map"""

    # DATA - Data register
    DATA_ADDR = 0x0004
    DATA_FIFO_POS = 0
    DATA_FIFO_MSK = 0xff
    DATA_FERR_POS = 16
    DATA_FERR_MSK = 0x1
    DATA_PERR_POS = 17
    DATA_PERR_MSK = 0x1

    # STAT - Status register
    STAT_ADDR = 0x000c
    STAT_BUSY_POS = 2
    STAT_BUSY_MSK = 0x1
    STAT_RXE_POS = 4
    STAT_RXE_MSK = 0x1
    STAT_TXF_POS = 8
    STAT_TXF_MSK = 0x1

    # CTRL - Control register
    CTRL_ADDR = 0x0010
    CTRL_BAUD_POS = 0
    CTRL_BAUD_MSK = 0x3
    CTRL_TXEN_POS = 4
    CTRL_TXEN_MSK = 0x1
    CTRL_RXEN_POS = 5
    CTRL_RXEN_MSK = 0x1
    CTRL_TXST_POS = 6
    CTRL_TXST_MSK = 0x1

    # LPMODE - Low power mode control
    LPMODE_ADDR = 0x0014
    LPMODE_DIV_POS = 0
    LPMODE_DIV_MSK = 0xff
    LPMODE_EN_POS = 31
    LPMODE_EN_MSK = 0x1

    # INTSTAT - Interrupt status register
    INTSTAT_ADDR = 0x0020
    INTSTAT_TX_POS = 0
    INTSTAT_TX_MSK = 0x1
    INTSTAT_RX_POS = 1
    INTSTAT_RX_MSK = 0x1

    # ID - IP-core ID register
    ID_ADDR = 0x0040
    ID_UID_POS = 0
    ID_UID_MSK = 0xffffffff

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
    def stat(self):
        """Status register"""
        return self._if.read(self.STAT_ADDR)

    @property
    def stat_bf(self):
        return _RegStat(self)

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
    def lpmode(self):
        """Low power mode control"""
        return self._if.read(self.LPMODE_ADDR)

    @lpmode.setter
    def lpmode(self, val):
        self._if.write(self.LPMODE_ADDR, val)

    @property
    def lpmode_bf(self):
        return _RegLpmode(self)

    @property
    def intstat(self):
        """Interrupt status register"""
        return self._if.read(self.INTSTAT_ADDR)

    @intstat.setter
    def intstat(self, val):
        self._if.write(self.INTSTAT_ADDR, val)

    @property
    def intstat_bf(self):
        return _RegIntstat(self)

    @property
    def id(self):
        """IP-core ID register"""
        return self._if.read(self.ID_ADDR)

    @property
    def id_bf(self):
        return _RegId(self)
