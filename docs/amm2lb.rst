.. _amm2lb:

=============================
Avalon-MM to Local Bus bridge
=============================

Signals
=======

============= ===== ========= =========================================================
Signal        Width Direction Description
============= ===== ========= =========================================================
clk           1     input     System clock
reset         1     input     System reset
address       >1    input     Avalon-MM address
read          1     input     Avalon-MM read
readdata      >1    output    Avalon-MM read data
readdatavalid 1     output    Avalon-MM read data valid
byteenable    >1    input     Avalon-MM byte enable
write         1     input     Avalon-MM write
writedata     >1    input     Avalon-MM write data
waitrequest   1     output    Avalon-MM wait request
waddr         >1    input     Local Bus write address bus
wdata         >1    input     Local Bus write data bus
wen           1     input     Local Bus write request enable signal
wstrb         >1    input     Local Bus write byte strobe bus (one bit for every write data byte)
wready        1     output    Local Bus write request ready signal
raddr         >1    input     Local Bus read address bus
ren           1     input     Local Bus read request enable signal
rdata         >1    output    Local Bus read data bus
rvalid        1     output    Local Bus read data valid signal
============= ===== ========= =========================================================

.. note::

    Specific bit widths for buses are defined in configuration section of a CSR map description file.

Protocol
========

Refer to official Intel documentation: `Avalon® Interface Specifications <https://www.intel.com/content/dam/www/programmable/us/en/pdfs/literature/manual/mnl_avalon_spec.pdf>`_.
