.. _config:

==================
Configuration file
==================

Corsair uses simple flat INI configuration file called ``csrconfig``. It is used for the two things:

- to pass global parameters to corsair
- to specify all generation targets with their attributes

Example of csrconfig is below:

.. code-block:: ini

    [globcfg]
    data_width = 32
    address_width = 16
    register_reset = sync_pos

    [v_module]
    path = regs.v
    interface = axil
    generator = Verilog

    [c_header]
    path = regs.h
    generator = CHeader

It has one special section ``globcfg`` for global parameters, and one or many sections for generation targets.

globcfg section
===============

Global parameters available:

+-----------------------+----------------+-----------------------------------------------------------------------------------------------------+
| Parameter             | Default value  | Description                                                                                         |
+=======================+================+=====================================================================================================+
| ``base_address``      | 0              | Register map base address in global address map                                                     |
+-----------------------+----------------+-----------------------------------------------------------------------------------------------------+
| ``data_width``        | 32             | Width of all data buses and registers                                                               |
+-----------------------+----------------+-----------------------------------------------------------------------------------------------------+
| ``address_width``     | 16             | Address bus width (capacity of the register map)                                                    |
+-----------------------+----------------+-----------------------------------------------------------------------------------------------------+
| ``register_reset``    | ``sync_pos``   | Flip-flop reset style                                                                               |
|                       |                +---------------+-------------------------------------------------------------------------------------+
|                       |                | ``sync_pos``  | Synchronous active high reset                                                       |
|                       |                +---------------+-------------------------------------------------------------------------------------+
|                       |                | ``sync_neg``  | Synchronous active low reset                                                        |
|                       |                +---------------+-------------------------------------------------------------------------------------+
|                       |                | ``async_pos`` | Asynchronous active high reset                                                      |
|                       |                +---------------+-------------------------------------------------------------------------------------+
|                       |                | ``async_neg`` | Asynchronous active low reset                                                       |
+-----------------------+----------------+---------------+-------------------------------------------------------------------------------------+
| ``address_increment`` | ``none``       | Address auto increment mode, if no address is provided for a register                               |
|                       |                +------------------------+----------------------------------------------------------------------------+
|                       |                | ``none``               | Address auto increment mode is disabled                                    |
|                       |                +------------------------+----------------------------------------------------------------------------+
|                       |                | ``data_width``         | Enable address auto increment with value based on ``globcfg.data_width``   |
|                       |                +------------------------+----------------------------------------------------------------------------+
|                       |                | ``<positive-integer>`` | Enable address auto increment with provided number of bytes, e.g 4         |
+-----------------------+----------------+------------------------+----------------------------------------------------------------------------+
| ``address_alignment`` | ``data_width`` | Check for address alignment of registers.                                                           |
|                       |                +------------------------+----------------------------------------------------------------------------+
|                       |                | ``none``               | No check of address alignment                                              |
|                       |                +------------------------+----------------------------------------------------------------------------+
|                       |                | ``data_width``         | Enable check of address alignment based on ``globcfg.data_width``          |
|                       |                +------------------------+----------------------------------------------------------------------------+
|                       |                | ``<positive-integer>`` | Enable check of address alignment based on provided number of bytes, e.g 4 |
+-----------------------+----------------+------------------------+----------------------------------------------------------------------------+
| ``force_name_case``   | ``none``       | Force case for all the names (regsiters, bit fields, enums)                                         |
|                       |                +-----------+-----------------------------------------------------------------------------------------+
|                       |                | ``none``  | Names used as they are                                                                  |
|                       |                +-----------+-----------------------------------------------------------------------------------------+
|                       |                | ``lower`` | Force names to have lowercase                                                           |
|                       |                +-----------+-----------------------------------------------------------------------------------------+
|                       |                | ``upper`` | Force names to have uppercase                                                           |
+-----------------------+----------------+-----------+-----------------------------------------------------------------------------------------+

You can omit any of this in your ``csrconfig`` file - default value will be used.

You also can add your own parameters and access them inside your custom flow the same way as standart ones. This is valid config:

.. code-block:: ini

    [globcfg]
    data_width = 32
    address_width = 16
    register_reset = sync_pos
    foo = bar

Target sections
===============

Target section defines file generator and specify its parameters.
Generator is a Python class that produces some output based on input arguments.
Usually, one target section - one output file.

Few simple rules to remember:

* target name should be unique
* targets without ``generator`` parameter is ignored

Parameter ``generator`` can be defined in the two ways. To use built-in generator:

.. code-block:: ini

    [target]
    generator = Verilog

Or to use custom created one:

.. code-block:: ini

    [target]
    generator = custom_generator.py::MyCustomGenerator

If you are interesting in expanding corsair functionality, there is the `example <https://github.com/esynr3z/corsair/tree/master/examples/custom_generator>`_ of how to build your own
generator and use it with corsair CLI.

Generators
==========

Corsair provides many built-in generators:

======================== ================================================================
Generator                Description
======================== ================================================================
``Json``                 Dump register map to a JSON file
``Yaml``                 Dump register map to a YAML file
``Txt``                  Dump register map to a text file
``Verilog``              Create Verilog file with register map
``Vhdl``                 Create VHDL file with register map
``VerilogHeader``        Create Verilog header file with register map defines
``CHeader``              Create C header file with register map define
``SystemVerilogPackage`` Create SystemVerilog package with register map parameters
``Markdown``             Create documentation for a register map in Markdown
``Asciidoc``             Create documentation for a register map in AsciiDoc
``Python``               Create Python file with register map
======================== ================================================================

There are even more generators but these ones are normally don't used in ``csrconfig`` file -
they are helpfull for creating custom generators or other development tasks:

======================== ================================================================
Generator                Description
======================== ================================================================
``Generator``            Base generator class
``Jinja2``               Basic class for rendering Jinja2 templates
``Wavedrom``             Basic class for rendering register images with wavedrom
``LbBridgeVerilog``      Create Verilog file with bridge to Local Bus
``LbBridgeVhdl``         Create Vhdl file with bridge to Local Bus
======================== ================================================================

.. note::

    These parameters in ``csrconfig`` file are nothing but arguments for the class constructor.
    If parameter is not provided - default value will be used.
    Please note that the tables below were created mannualy, while data in :ref:`Generators API <generators-api>` page was collected automaticaly.
    As these things are exactrly the same information just in different forms, please refer to API if you have any doubts.

Json
----
========== ============= ================================================================
Parameter  Default       Description
========== ============= ================================================================
``path``   ``regs.json`` Path to the output file
========== ============= ================================================================

Yaml
----
========== ============= ================================================================
Parameter  Default       Description
========== ============= ================================================================
``path``   ``regs.yaml`` Path to the output file
========== ============= ================================================================

Txt
---
========== ============= ================================================================
Parameter  Default       Description
========== ============= ================================================================
``path``   ``regs.txt``  Path to the output file
========== ============= ================================================================

Verilog
-------
+-----------------+------------+-----------------------------------------------------+
| Parameter       | Default    | Description                                         |
+=================+============+=====================================================+
| ``path``        | ``regs.v`` | Path to the output file                             |
+-----------------+------------+-----------------------------------------------------+
| ``read_filler`` | 0          | Numeric value to return if wrong address was read   |
+-----------------+------------+-----------------------------------------------------+
| ``interface``   | ``axil``   | Register map bus protocol                           |
|                 |            +-----------+-----------------------------------------+
|                 |            | ``axil``  | AXI4-Lite                               |
|                 |            +-----------+-----------------------------------------+
|                 |            | ``amm``   | Avalon-MM                               |
|                 |            +-----------+-----------------------------------------+
|                 |            | ``apb``   | APB4                                    |
|                 |            +-----------+-----------------------------------------+
|                 |            | ``lb``    | Custom LocalBus interface               |
+-----------------+------------+-----------+-----------------------------------------+

Vhdl
----
+-----------------+---------------+-----------------------------------------------------+
| Parameter       | Default       | Description                                         |
+=================+===============+=====================================================+
| ``path``        | ``regs.vhd``  | Path to the output file                             |
+-----------------+---------------+-----------------------------------------------------+
| ``read_filler`` | 0             | Numeric value to return if wrong address was read   |
+-----------------+---------------+-----------------------------------------------------+
| ``interface``   | ``axil``      | Register map bus protocol                           |
|                 |               +-----------+-----------------------------------------+
|                 |               | ``axil``  | AXI4-Lite                               |
|                 |               +-----------+-----------------------------------------+
|                 |               | ``amm``   | Avalon-MM                               |
|                 |               +-----------+-----------------------------------------+
|                 |               | ``apb``   | APB4                                    |
|                 |               +-----------+-----------------------------------------+
|                 |               | ``lb``    | Custom LocalBus interface               |
+-----------------+---------------+-----------+-----------------------------------------+

VerilogHeader
-------------
========== ============= ================================================================
Parameter  Default       Description
========== ============= ================================================================
``path``   ``regs.vh``   Path to the output file
``preifx`` ``CSR``       Prefix for all defines. If empty, output file name will be used.
========== ============= ================================================================

CHeader
-------
========== ============= ================================================================
Parameter  Default       Description
========== ============= ================================================================
``path``   ``regs.h``    Path to the output file
``preifx`` ``CSR``       Prefix for all defines. If empty, output file name will be used.
========== ============= ================================================================

SystemVerilogPackage
--------------------
========== =============== ================================================================
Parameter  Default         Description
========== =============== ================================================================
``path``   ``regs_pkg.sv`` Path to the output file
``preifx`` ``CSR``         Prefix for the all parameters. If empty, output file name will be used.
========== =============== ================================================================

Markdown
--------
===================== ================ ================================================================
Parameter             Default          Description
===================== ================ ================================================================
``path``              ``regs.md``      Path to the output file
``title``             ``Register map`` Document title
``print_images``      ``True``         Enable generating images for bit fields of a register
``image_dir``         ``regs_img``     Path to directory where all images will be saved
``print_conventions`` ``True``         Enable generating table with register access modes explained
===================== ================ ================================================================

Asciidoc
--------
===================== ================ ================================================================
Parameter             Default          Description
===================== ================ ================================================================
``path``              ``regs.md``      Path to the output file
``title``             ``Register map`` Document title
``print_images``      ``True``         Enable generating images for bit fields of a register
``image_dir``         ``regs_img``     Path to directory where all images will be saved
``print_conventions`` ``True``         Enable generating table with register access modes explained
===================== ================ ================================================================

Python
------
========== ============= ================================================================
Parameter  Default       Description
========== ============= ================================================================
``path``   ``regs.py``   Path to the output file
========== ============= ================================================================
