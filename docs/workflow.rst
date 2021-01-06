.. _workflow:

========
Workflow
========

Standalone (CLI)
================

It is as easy as:

* Create CSR map description file or generate a template with Corsair:

::

    corsair --template-regmap regs.json

* Make changes to ``regs.json``
* Generate output artifacts:

::

    corsair -r regs.json --hdl --lb-bridge --docs

* You will get:
    * Register map HDL code
    * Bridge to some standart interface (e.g. AXI-Lite)
    * Document, describing the map

Use -h/--help key to get all options available.

Refer to :ref:`Register map description file <csr-map>` part to get details about input description file.

Integration
-----------

All generated register maps support only Local Bus interface to make code generation and integration more uniform. Local Bus is a custom interface designed to be simple and easy to create bridge to any popular memmory-mapped interface such as APB, AXI-Lite or Avalon-MM.

.. image:: local_bus.svg
    :alt: Local Bus architecture
    :align: center

Follow to :ref:`Local Bus specification <csr-map>` for a details.

Import (Python)
===============

Corsair can be imported to your Python module to enable creation of a custom workflow.

::

    import corsair

    # create and fill the CSR map
    config = corsair.Configuration()
    config['lb_bridge']['type'] = 'axil'

    reg_a = corsair.Register('rega', address=4)
    reg_a.add_bfields(corsair.BitField('bfa', lsb=0, width=8))

    rmap = corsair.RegisterMap(config)
    rmap.add_regs(reg_a)

    # do your custom processing
    rmap_custom_processig(rmap)
    
More information can be found in the API section:

* :ref:`Configuration <config-api>`
* :ref:`Register map <regmap-api>`
* :ref:`Readers <readers-api>`
* :ref:`Writers <writers-api>`
