.. _apb:

===
APB
===

Signals
=======

These signals will be used in the interface of the register map.

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
========= ===== ========= =========================================================

.. note::

    Specific bit widths for buses are defined in ``globcfg`` section of a ``csrconfig`` file.

Implementation details:

* APB4 slave
* ``pprot`` signal is not implemented
* ``pslverr`` tied to 0 - slave is always ``OKAY``

Protocol
========

Refer to official ARM documentation: `IHI0024C AMBA® APB Protocol Version: 2.0 <https://developer.arm.com/documentation/ihi0024/latest/>`_.
