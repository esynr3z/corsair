.. _csr-map:

=============================
Register map description file
=============================

Overview
========

Register map description file is the only input file of Corsair in fact. It consists of two parts: ``config`` and ``regmap``. ``config`` is a collection (dictionary) of global parameters to control the whole generation process. And ``regmap`` is a simply list of registers.


You can use special key to create register map template in any supported format (JSON or YAML, currently):

::

    corsair --template-regmap template_csr.json


``config`` part can be stored (fully or partially) in a separate file. It enables to share one configuration with several maps. To provide separate configuration file use ```-c/--config`` key:

::

    corsair --config config.json

To create template of configuration file:

::

    corsair --template-config config.json

Configurations are aplied one by one - every next is merged with previous one with values to be overwritten.
In the other words, the sequence or priority (from lowest to highest) is default configuration, then configuration from separate file and configuration from register map file finally. For example, for ``corsair -r map.json -c config.json`` command:

* Configuration with default values are created.
* If presents, separate configuration file (``-c/--config`` key) is merged with default configuration. New values are written over older ones.
* If ``config`` section presents in register map file (``-r/--regmap`` key), this configuration is merged with one from previous step.

Configuration
=============

Configuration is collection with global parameters to control the whole generation process. It may be represented as item under ``config`` label inside register map description file, or/and as separate file (fully or partially).

List of default parameters and groups (relative to configuration root):

* name
* version
* register_reset
* data_width
* address_width
* regmap
    * read_filler
    * address_increment_mode
    * address_increment_value
    * address_alignment_mode
    * address_alignment_value
* lb_bridge
    * type
    * py_driver
* docs
    * register_images
    * print_conventions

name
----

Base name of the register map. Will be used as basic name to create names for all output artifacts.

**Default value**: "".

.. note::
    If no name is provided, name of a register map description file (or configuration file) will be used instead.

version
-------

Version of the register map.

**Default value**: "1.0".

register_reset
--------------

Type of a reset being used.

Choice of:

==================== ================================================================
``register_reset``   Description
==================== ================================================================
"sync_pos"           Synchronous active high reset
"sync_neg"           Synchronous active low reset
"async_pos"          Asynchronous active high reset
"async_neg"          Asynchronous active low reset
==================== ================================================================

**Default value**: "sync_pos".

data_width
----------

Bit width of data buses to be used inside register map.

**Default value**: 32.

address_width
-------------

Bit width of address buses to be used inside register map.

**Default value**: 32.


regmap
------

Group of parameters related to register map HDL module.

=========================== ============ ==========================================================================
Parameter                   Default      Description
=========================== ============ ==========================================================================
``read_filler``             0            Value to be returned if read of empty address or WO register is performed.
``address_increment_mode``  "none"       Address auto increment mode, if no address is provided for a register
``address_increment_value`` 4            Auto increment with provided value: 1 - 1 byte, 4 - 4 bytes, etc
``address_alignment_mode``  "data_width" Check for address alignment.
``address_alignment_value`` 4            Address alignment with provided value: 1 - 1 byte, 4 - 4 bytes, etc
=========================== ============ ==========================================================================

Options for ``address_increment_mode``:

========================== ========================================================================================
``address_increment_mode`` Description
========================== ========================================================================================
"none"                     No address auto increment. If no address is provided, error will be generated.
"data_width"               Enable auto increment with value based on ``data_width``
"custom"                   Enable auto increment based on ``address_increment_value``
========================== ========================================================================================

Options for ``address_alignment_mode``:

========================== =========================================================================================
``address_alignment_mode`` Description
========================== =========================================================================================
"none"                     No check of address alignment
"data_width"               Enable check of address alignment based on ``data_width``
"custom"                   Enable check of address alignment based on ``address_alignment_value``
========================== =========================================================================================

lb_bridge
---------

Group of parameters related to interface bridge to Local Bus HDL module.

================= ========= =========================================
Parameter         Default   Description
================= ========= =========================================
``type``          "none"    Interface type. One of the options below.
``py_driver``     ``false`` Generate Python drivers for the bridge. Valid only when ``type`` is "spi".
================= ========= =========================================

Options for ``type``:

======== ==========================
``type`` Description
======== ==========================
"amm"    Avalon-MM interface
"apb"    APB4 interface
"axil"   AXI4-Lite interface
"spi"    SPI interface
"none"   For Local Bus directly use
======== ==========================

.. note::
    More details about Local Bus interface can be found in :ref:`Local Bus <local-bus>`.

Allowed combinations of the parameters:

======== ============================= =================
``type`` ``data_width``                ``address_width``
======== ============================= =================
"amm"    8, 16, ..., 1024 (power of 2) 1 - 64
"apb"    8, 16, 32                     1 - 32
"axil"   32, 64                        32, 64
"spi"    8, 16, 32                     8, 16, 32
"none"   8, 16, ... (any power of 2)   1 - 64
======== ============================= =================

docs
----

Group of parameters related to documentation generation.

===================== ========= =======================================================================
Parameter             Default   Description
===================== ========= =======================================================================
``register_images``   ``true``  Generate graphic representation of register's bitfields
``print_conventions`` ``true``  Print bitfields conventions for ``access`` and ``modifiers`` attributes
===================== ========= =======================================================================

Register map
============

Register map consists of registers (named addresses in a address map). And registers are made of bit fields - group of bits with special properties.
When register is accessed, collection of bit fields being read or written, actually.

List of registers stored in a ``regmap`` item inside register map description file.

Register
--------

Register related attributes:

================== ======= ============================================================================================================
Attribute          Default Description
================== ======= ============================================================================================================
``name``           ""      Register name
``description``    ""      Register description
``address``        0       Register address
``access_strobes`` False   Enable pulse generation on special outputs on every read or write
``complementary``  False   Enable complementary mode: two opposite registers (with RO or WO fields only) can be assigned to one address
``write_lock``     False   Enable write lock: when special signal is asserted, register will ignore all write transactions
``bfields``        []      Array with register bit fields
================== ======= ============================================================================================================

.. note::
    Name and description can be ommited if register is made from the only one bit field. Name and description of that field will be used instead of register's ones.

Bit field
---------

Field related attributes:

=============== ======= ================================================================================================
Parameter       Default Description
=============== ======= ================================================================================================
``name``           ""      Field name
``description``    ""      Field description
``initial``        0       Initial (reset) value for the field
``width``          1       Field width (bits)
``lsb``            0       Field LSB position
``access``         "rw"    Access mode for the field. One of the options below.
``modifiers``      []      Access modifiers. Choice of none or multiple options below.
=============== ======= ================================================================================================

Options for ``access``:

========== ===============================
``access`` Description
========== ===============================
"rw"       Read or Write.
"ro"       Read Only. Write has no effect.
"wo"       Write Only. Zeros are read.
========== ===============================

Options for ``modifiers``:

============= ===========================================================================================
``modifiers`` Description
============= ===========================================================================================
"sc"          Self Clear. Write 0 - no effect, write 1 - next tick self clear.
"w1tc"        Write 1 To Clear. Write 0 - no effect, write 1 - current value will be cleared (all zeros).
"w1ts"        Write 1 To Set. Write 0 - no effect, write 1 - current value will be set (all ones).
"w1tt"        Write 1 To Toggle. Write 0 - no effect, write 1 - current value will be inversed.
"rtc"         Read To Clear. Current value will be cleared next tick after read.
"const"       Constant. Reset value is hardcoded as only value can be read.
"hwu"         Hardware Update. Register value can be updated from outside the map with hardware.
"fifo"        FIFO memory. Access to a register will be transformed to transaction to an external FIFO.
============= ===========================================================================================


How ``modifiers`` can be combined with ``access``:

+------------+-------------------+
| ``access`` | ``modifiers``     |
+============+===================+
| "rw"       | [] (no modifiers) |
|            +-------------------+
|            | ["hwu"]           |
|            +-------------------+
|            | ["hwu", "w1tc"]   |
|            +-------------------+
|            | ["hwu", "w1ts"]   |
|            +-------------------+
|            | ["hwu", "w1tt"]   |
|            +-------------------+
|            | ["fifo"]          |
+------------+-------------------+
| "wo"       | [] (no modifiers) |
|            +-------------------+
|            | ["sc"]            |
|            +-------------------+
|            | ["fifo"]          |
+------------+-------------------+
| "ro"       | [] (no modifiers) |
|            +-------------------+
|            | ["const"]         |
|            +-------------------+
|            | ["hwu"]           |
|            +-------------------+
|            | ["hwu", "rtc"]    |
|            +-------------------+
|            | ["fifo"]          |
+------------+-------------------+
