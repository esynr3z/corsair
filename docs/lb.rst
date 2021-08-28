.. _lb:

========
LocalBus
========

LocalBus is a custom bus interface. You can use it for your register map, hovewer, it was designed specially
to simplify integrating more common bus interfaces to register map. It acts as internal "virtual" interface.

In fact, all other supported buses (APB, AXI-Lite and etc.) in corsair are nothing more than just bridges to LocalBus interface
under the hood.

Signals
=======

====== ===== ========= =========================================================
Signal Width Direction Description
====== ===== ========= =========================================================
waddr  >1    input     Write address bus
wdata  >1    input     Write data bus
wen    1     input     Write request enable signal
wstrb  >1    input     Write byte strobe bus (one bit for every write data byte)
wready 1     output    Write request ready signal
raddr  >1    input     Read address bus
ren    1     input     Read request enable signal
rdata  >1    output    Read data bus
rvalid 1     output    Read data valid signal
====== ===== ========= =========================================================

.. note::

    Specific bit widths for buses are defined in ``globcfg`` section of a ``csrconfig`` file.

Transfers
=========

Only simple single transfers are supported. No bursts or stream accesses. Every transfer can be extended with special signals.

Just for example, data bus is 32 bits wide for all the waveforms below.

Simple write
------------

Write data ``D0`` to address ``A0``.

.. wavedrom::

    {"signal": [
      {"name": "clk", "wave": "p...."},
      {"name": "waddr", "wave": "x3x..", "data": ["A0"]},
      {"name": "wdata[31:0]", "wave": "x4x..", "data": ["D0"]},
      {"name": "wen", "wave": "010.."},
      {"name": "wstrb[3:0]", "wave": "x3x..", "data": ["0xF"]},
      {"name": "wready", "wave": "1...."}
    ]}

Write with bytes strobes
------------------------

Byte strobe signalling to write only bytes 1 and 2 (``wstrb = 0x6 = 0b0110``) of ``D0`` word.

.. wavedrom::

    {"signal": [
      {"name": "clk", "wave": "p...."},
      {"name": "waddr", "wave": "x3x..", "data": ["A0"]},
      {"name": "wdata[31:0]", "wave": "x4x..", "data": ["D0"]},
      {"name": "wen", "wave": "010.."},
      {"name": "wstrb[3:0]", "wave": "x3x..", "data": ["0x6"]},
      {"name": "wready", "wave": "1...."}
    ]}

Write with wait states
----------------------

Write data ``D0`` to address ``A0``, then write ``D1`` to ``A1`` ends (``wen`` goes low) as soon as ``wready`` become high.

.. wavedrom::

    {"signal": [
      {"name": "clk", "wave": "p......."},
      {"name": "waddr", "wave": "x3x3..x.", "data": ["A0", "A1"]},
      {"name": "wdata[31:0]", "wave": "x4x4..x.", "data": ["D0", "D1"]},
      {"name": "wen", "wave": "0101..0."},
      {"name": "wstrb[3:0]", "wave": "x3x3..x.", "data": ["0xF", "0xF"]},
      {"name": "wready", "wave": "1.0..10."}
    ]}

Simple read
-----------

Read data ``D0`` from address ``A0``. Minimum response time - 1 tick. "Combinatoral" (in the same tick) read is not supported.
Read ends (``ren`` goes low) after ``rvalid`` is asserted.

.. wavedrom::

    {"signal": [
      {"name": "clk", "wave": "p....."},
      {"name": "raddr", "wave": "x3.x..", "data": ["A0"]},
      {"name": "ren", "wave": "01.0.."},
      {"name": "rdata[31:0]", "wave": "x.4x..", "data": ["D0"]},
      {"name": "rvalid", "wave": "0.10.."}
    ]}

Read with wait states
---------------------

Read data ``D0`` from address ``A0`` with 2 wait states.

.. wavedrom::

    {"signal": [
      {"name": "clk", "wave": "p......."},
      {"name": "raddr", "wave": "x3...x..", "data": ["A0"]},
      {"name": "ren", "wave": "01...0.."},
      {"name": "rdata[31:0]", "wave": "x...4x..", "data": ["D0"]},
      {"name": "rvalid", "wave": "0...10.."}
    ]}