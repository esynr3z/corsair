.. _csr-map:

========================
CSR map description file
========================

General structure
=================

CSR map description file consists of two parts: ``configuration`` and ``registers``. ``configuration`` is a collection (dictionary) of global parameters to control the whole generation process. And ``registers`` is a simply list of CSRs.

Schematic representation of the structure is below (``{}`` is for a dictionary, ``[]`` - for a list). Description files in JSON or YAML formats follow in particular that structure with almost no changes.

* name
* version
* configuration: {}
    * parameter_a
    * parameter_group_b {}
        * parameter_c
        * parameter_d
    * parameter_e
* register_map []
    * register_map[0] {}
        * name
        * ...
        * bit_fields []
            * bit_fields[0] {}
                * name
                * ...
            * bit_fields[1] {}
                * name
                * ...
    * register_map[1] {}
    * ...

You can use ``-t`` key to create CSR map description file template in any supported format:

::

    corsair -t template_csr.json


Configuration
=============

List of default parameters and groups (relative to configuration root):

* read_filler
* address_calculation
    * auto_increment_mode
    * auto_increment_value
    * alignment_mode
    * alignment_value
* register_reset
* interface_generic
    * type
    * data_width
    * address_width
* interface_specific

read_filler
-----------

Value to be returned if read of empty address or WO register is performed.

**Default value**: 0.

address_calculation
-------------------

Group of address calculation related parameters.

======================== ============ ======================================================================
Parameter                Default      Description
======================== ============ ======================================================================
``auto_increment_mode``  "none"       Address auto increment mode, if no address is provided for a register
``auto_increment_value`` 4            Auto increment with provided value: 1 - 1 byte, 4 - 4 bytes, etc
``alignment_mode``       "data_width" Check for address alignment.
``alignment_value``      4            Address alignment with provided value: 1 - 1 byte, 4 - 4 bytes, etc
======================== ============ ======================================================================

Options for ``auto_increment_mode``:

======================= ========================================================================================
``auto_increment_mode`` Description
======================= ========================================================================================
"none"                  No address auto increment. If no address is provided, error will be generated.
"data_width"            Enable auto increment with value based on ``data_width`` of ``interface_generic`` group
"custom"                Enable auto increment based on ``auto_increment_value``
======================= ========================================================================================

Options for ``alignment_mode``:

==================== =========================================================================================
``alignment_mode``   Description
==================== =========================================================================================
"none"               No check of address alignment
"data_width"         Enable check of address alignment based on ``data_width`` of ``interface_generic`` group
"custom"             Enable check of address alignment based on ``alignment_value``
==================== =========================================================================================

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
"init_only"          No register reset. Declaration with initialization will be used.
==================== ================================================================

**Default value**: "sync_pos".

interface_generic
-----------------

Group of generic interface related parameters.

================= ======= =========================================
Parameter         Default Description
================= ======= =========================================
``type``          "lb"    Interface type. One of the options below.
``data_width``    32      Data bus bit width
``address_width`` 32      Address bus bit width
================= ======= =========================================

Options for ``type``:

======== ====================
``type`` Description
======== ====================
"amm"    Avalon-MM interface.
"apb"    APB4 interface.
"axil"   AXI4-Lite interface
"lb"     Local Bus interface.
======== ====================

.. note::
    More details about Local Bus interface can be found in :ref:`Local Bus <local-bus>`.

Allowed combinations of the parameters:

======== ============================= =================
``type`` ``data_width``                ``address_width``
======== ============================= =================
"amm"    8, 16, ..., 1024 (power of 2) 1 - 64
"apb"    8, 16, 32                     1 - 32
"axil"   32, 64                        32, 64
"lb"     8, 16, ... (any power of 2)   1 - 64
======== ============================= =================

interface_specific
------------------

Group of interface type specific parameters. This block is unque for every interface type.

Registers
=========

List of CSRs.

Register
--------

Register related attributes:

=============== ======= ==============================
Attribute       Default Description
=============== ======= ==============================
``name``        ""      Register name
``description`` ""      Register description
``address``     0       Register address
``bit_fields``  []      Array with register bit_fields
=============== ======= ==============================

.. note::
    Name and description can be ommited if register is made from the only one bit field. Name and description of that field will be used instead of register's ones.

Bit field
---------

Field related attributes:

================ ======= ================================================================================================
Parameter        Default Description
================ ======= ================================================================================================
``name``         ""      Field name
``description``  ""      Field description
``initial``      0       Initial (reset) value for the field
``width``        1       Field width (bits)
``lsb``          0       Field LSB position
``access``       "rw"    Access mode for the field. One of the options below.
``access_flags`` False   Enable pulse generation on output "read_access" or "write_access" signals on every read or write
``modifiers``    []      Access modifiers. Choice of none or multiple options below.
================ ======= ================================================================================================

Options for ``access``:

========== =====================
``access`` Description
========== =====================
"rw"       Read and Write access
"ro"       Read only
"wo"       Write only
========== =====================

Options for ``modifiers``:

================== ===========================================================================================================================================
``modifiers``      Description
================== ===========================================================================================================================================
"self_clear"       Write 0 - no effect, write 1 - next tick self clear.
"write1_to_clear"  Write 0 - no effect, write 1 - current value will be cleared.
"write1_to_toggle" Write 0 - no effect, write 1 - current value will be inversed.
"read_to_clear"    Any CSR read - current value will be cleared.
"read_const"       Use "initial" as only value can be readen.
"external_update"  Register can be updated outside the map with some "data" bus and "update" signal.
"memory"           Access to memory. Read with some "data" bus, "read_enable" and "data_valid" signals. Write with some "data" bus and "write_enable" signals.
================== ===========================================================================================================================================


How ``modifiers`` can be combined with ``access``:

+------------+-------------------------------------------+
| ``access`` | ``modifiers``                             |
+============+===========================================+
| "rw"       | [] (no modifiers)                         |
|            +-------------------------------------------+
|            | ["external_update"]                       |
|            +-------------------------------------------+
|            | ["external_update", "write1_to_clear"]    |
|            +-------------------------------------------+
|            | ["external_update", "write1_to_toggle"]   |
|            +-------------------------------------------+
|            | ["memory"]                                |
+------------+-------------------------------------------+
| "wo"       | [] (no modifiers)                         |
|            +-------------------------------------------+
|            | ["self_clear"]                            |
|            +-------------------------------------------+
|            | ["memory"]                                |
+------------+-------------------------------------------+
| "ro"       | [] (no modifiers)                         |
|            +-------------------------------------------+
|            | ["read_const"]                            |
|            +-------------------------------------------+
|            | ["external_update"]                       |
|            +-------------------------------------------+
|            | ["external_update", "read_to_clear"]      |
|            +-------------------------------------------+
|            | ["memory"]                                |
+------------+-------------------------------------------+
