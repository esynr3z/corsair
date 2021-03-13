.. _spi2lb:

=======================
SPI to Local Bus bridge
=======================

Special bridge that can be useful for some core-less projects.
Just put all the design's control and status information into a register map, add this bridge and rule your FPGA from PC / MCU / other FPGA.

Example of a such design can be found in the main `repository <https://github.com/esynr3z/corsair/tree/master/examples/spi_regs>`_.

Signals
=======

========= ===== ========= =========================================================
Signal    Width Direction Description
========= ===== ========= =========================================================
clk       1     input     System clock
rst       1     input     System reset
spi_sck   1     input     SPI clock from master
spi_cs_n  1     input     SPI chip select from master (active low)
spi_mosi  1     input     SPI data from master
spi_miso  1     output    SPI data to master
lb_waddr  >1    input     Local Bus write address bus
lb_wdata  >1    input     Local Bus write data bus
lb_wen    1     input     Local Bus write request enable signal
lb_wstrb  >1    input     Local Bus write byte strobe bus (one bit for every write data byte)
lb_wready 1     output    Local Bus write request ready signal
lb_raddr  >1    input     Local Bus read address bus
lb_ren    1     input     Local Bus read request enable signal
lb_rdata  >1    output    Local Bus read data bus
lb_rvalid 1     output    Local Bus read data valid signal
========= ===== ========= =========================================================

.. note::

    Specific bit widths for buses are defined in configuration section of a CSR map description file.

Parameters
==========

Some generic SPI parameters:

* SPI slave
* mode 0 only:
    * clock polarity - low in idle state
    * clock phase - data sampled on rising edge and shifted out on the falling edge
* most significant bit (MSB) is transmitted first
* byte order from high to low
* ``spi_sck`` frequency must at least 8 times lower than ``clk`` frequency

Parameters related to code generation:

* Set ``lb_bridge.type`` parameter to  ``"spi"`` to select this bridge
* Address width is controlled with ``address_width`` parameter
* Data width is controlled with ``data_width`` parameter
* Python drivers (`pyftdi <https://pypi.org/project/pyftdi/>`_-based) generation can be enabled with ``lb_bridge.py_driver`` being set to ``true``

Transfers
=========

Just for example, data is 16 bits wide and address is 8 bits wide.

Write
-----

* Write 16-bit data ``D15-D0`` to 8-bit address ``A7-A0``.
* Control byte MSB is 1 (write opeartion).
* ``WB1``, ``WB0`` - write byte strobes (being set to 1 to write all the bytes).

.. wavedrom::

    {"signal": [
        {"name": "spi_sck", "wave": "0..HLHL|.HLHL|.HLHL.HLHL|.HL.."},
        {"name": "spi_cs_n", "wave": "10...........................1"},
        {"name": "spi_mosi", "wave": "0.3.3.3|3.4.4|4.4.5..5.5|5.0..", "data": ["A7", "A6", "", "A0", "WR=1", "", "WB1=1", "WB0=1", "D15", "D14", "", "D0"]},
        {"name": "spi_miso", "wave": "0............................."},
        {},
        {"name": "SPI", "wave": "x.3.......4.......5........x..", "data": ["Address", "Control byte", "Data word"]},
        {"name": "LocalBus", "wave": "x..........................2..", "data": ["Write"]}
    ]}

Write transaction on LocalBus starts right after last data bit is received and should be ended before next SPI transfer.
There is no back-pressure mechanisms in SPI, so possible collisions should be prevented by proper system design.

Read
----

* Read 16-bit data ``D15-D0`` from 8-bit address ``A7-A0``.
* Control byte MSB is 0 (read opeartion).
* ``WB1``, ``WB0`` - write byte strobes are always set to 0 when read is performing.

.. wavedrom::

    {"signal": [
        {"name": "spi_sck", "wave": "0..HLHL|.HLHL|.HLHL.HLHL|.HL.."},
        {"name": "spi_cs_n", "wave": "10...........................1"},
        {"name": "spi_mosi", "wave": "0.3.3.3|3.4.4|4.4.0...........", "data": ["A7", "A6", "", "A0", "RD=0", "", "WB1=0", "WB0=0"]},
        {"name": "spi_miso", "wave": "0..................5.5.5|5.0..", "data": ["D15", "D14", "", "D0"]},
        {},
        {"name": "SPI", "wave": "x.3.......4.......5........x..", "data": ["Address", "Control byte", "Data word"]},
        {"name": "LocalBus", "wave": "x...........2.....x...........", "data": ["Read"]}
    ]}

Read transaction on LocalBus starts right after MSB of control byte is received and should be ended before data to be transmitted to ``spi_miso``.
There is no back-pressure mechanisms in SPI, so possible collisions should be prevented by proper system design.
