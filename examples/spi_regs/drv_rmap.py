#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Created with Corsair vgit-latest

Python driver to access FPGA register map via SPI.
"""

import pyftdi.ftdi
import pyftdi.spi


def ftdi_show_devices():
    return pyftdi.ftdi.Ftdi.show_devices()


class FtdiSpi:
    ADDR_W = 8
    DATA_W = 16
    CTRL_W = 8

    ADDR_MSK = 2 ** ADDR_W - 1
    ADDR_BYTES = ADDR_W // 8 + (1 if ADDR_W % 8 else 0)
    DATA_MSK = 2 ** DATA_W - 1
    DATA_BYTES = DATA_W // 8 + (1 if DATA_W % 8 else 0)
    CTRL_MSK = 2 ** CTRL_W - 1
    CTRL_BYTES = CTRL_W // 8 + (1 if CTRL_W % 8 else 0)
    STRB_W = DATA_W // 8
    STRB_MSK = 2 ** STRB_W - 1

    def __init__(self, ftdi_url, cs=0, spi_freq=1E6):
        """Configure the FTDI interface.

        Keyword arguments:
         ftdi_url -- device url, which can be obtained by ftdi_show_devices()
         cs -- chip select number: A*BUS3 = 0, A*BUS4 = 1, ...
         freq -- SPI frequency in Hz
        """
        # Configure SPI master
        self._spi_ctrl = pyftdi.spi.SpiController(cs_count=cs + 1)
        self._spi_ctrl.configure(ftdi_url)
        self._spi_port = self._spi_ctrl.get_port(cs=cs, freq=spi_freq, mode=0)

    def _int_to_bytes(self, i, length=1):
        return int.to_bytes(i, length=length, byteorder='big', signed=False)

    def _bytes_to_int(self, b):
        return int.from_bytes(b, byteorder='big', signed=False)

    def read(self, addr):
        addr_b = self._int_to_bytes(addr & self.ADDR_MSK, self.ADDR_BYTES)
        ctrl_b = self._int_to_bytes(0, self.CTRL_BYTES)
        data_b = self._spi_port.exchange(addr_b + ctrl_b, self.DATA_BYTES)
        return self._bytes_to_int(data_b) & self.DATA_MSK

    def write(self, addr, data, strb=-1):
        addr_b = self._int_to_bytes(addr & self.ADDR_MSK, self.ADDR_BYTES)
        ctrl_b = self._int_to_bytes((1 << (self.CTRL_W - 1)) | (strb & self.STRB_MSK), self.CTRL_BYTES)
        data_b = self._int_to_bytes(data & self.DATA_MSK, self.DATA_BYTES)
        self._spi_port.exchange(addr_b + ctrl_b + data_b)

    def close_connection(self):
        self._spi_ctrl.terminate()


class Fpga:
    def __init__(self, rmap):
        """Initialize FPGA driver.

        Keyword arguments:
         rmap -- Register Map created with PyRegisterMapWriter
        """
        self.rmap = rmap
        self.spi = rmap._if

    def disconnect(self):
        """Disconnect from FTDI and close all open ports"""
        self.spi.close_connection()


if __name__ == "__main__":
    ftdi_show_devices()
