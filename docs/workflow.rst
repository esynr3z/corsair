.. _workflow:

========
Workflow
========

Standalone (CLI)
================

It is as easy as:

* Create CSR map description file or generate a template with Corsair:

::

    corsair -t ip_csr.json

* Make changes to ``ip_csr.json``
* Generate output artifacts:

::

    corsair -i ip_csr.json -o ip_regmap.v ip_regmap.md ip_regmap.h


Use -h/--help key to get all options available.

Import (Python)
===============

Corsair can be imported to your Python module to enable creation of a custom workflow.

::

    import corsair

    # create and fill the CSR map
    config = corsair.Configuration()
    config['interface_generic']['type'] = 'axil'

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
