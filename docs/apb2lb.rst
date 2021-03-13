.. _apb2lb:

=======================
APB to Local Bus bridge
=======================

Signals
=======

========= ===== ========= =========================================================
Signal    Width Direction Description
========= ===== ========= =========================================================
psel      1     input     APB select
paddr     >1    input     APB address
penable   1     input     APB enable
pwrite    1     input     APB write
pwdata    >1    input     APB write data
pstrb     >1    input     APB write strobe
prdata    >1    output    APB read data
pready    1     output    APB ready
pslverr   1     output    APB slave error
waddr     >1    input     Local Bus write address bus
wdata     >1    input     Local Bus write data bus
wen       1     input     Local Bus write request enable signal
wstrb     >1    input     Local Bus write byte strobe bus (one bit for every write data byte)
wready    1     output    Local Bus write request ready signal
raddr     >1    input     Local Bus read address bus
ren       1     input     Local Bus read request enable signal
rdata     >1    output    Local Bus read data bus
rvalid    1     output    Local Bus read data valid signal
========= ===== ========= =========================================================

.. note::

    Specific bit widths for buses are defined in configuration section of a CSR map description file.

Implementation details:

* APB4 slave
* ``pprot`` signal is not implemented
* ``pslverr`` tied to 0 - slave is always ``OKAY``

Protocol
========

Refer to official ARM documentation: `IHI0024C AMBA® APB Protocol Version: 2.0 <https://developer.arm.com/documentation/ihi0024/latest/>`_.
