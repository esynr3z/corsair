.. _amm:

=========
Avalon-MM
=========

Signals
=======

These signals will be used in the interface of the register map.

============= ===== ========= =========================================================
Signal        Width Direction Description
============= ===== ========= =========================================================
address       >1    input     Avalon-MM address
read          1     input     Avalon-MM read
readdata      >1    output    Avalon-MM read data
readdatavalid 1     output    Avalon-MM read data valid
byteenable    >1    input     Avalon-MM byte enable
write         1     input     Avalon-MM write
writedata     >1    input     Avalon-MM write data
waitrequest   1     output    Avalon-MM wait request
============= ===== ========= =========================================================

.. note::

    Specific bit widths for buses are defined in ``globcfg`` section of a ``csrconfig`` file.

Protocol
========

Refer to official Intel documentation: `Avalon® Interface Specifications <https://www.intel.com/content/dam/www/programmable/us/en/pdfs/literature/manual/mnl_avalon_spec.pdf>`_.
