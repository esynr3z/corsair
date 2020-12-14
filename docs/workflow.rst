.. _workflow:

========
Workflow
========

Run from command line
=====================

It is as easy as:

* Create CSR map description file or generate a template with Corsair:

::

    corsair -t ip_csr.json

* Make changes to ``ip_csr.json``
* Generate output artifacts:

::

    corsair -i ip_csr.json -o ip_regmap.v ip_regmap.md ip_regmap.h


Use -h/--help key to get all options allowed.

::

    $ python3 -m corsair -h
    usage: corsair [-h] [-v] [-i file[,ReaderClassName]]
                   [-o file[,WriterClassName] [file[,WriterClassName] ...]]
                   [-t file[,WriterClassName]]

    Control and status register (CSR) map generator for FPGA/ASIC projects.

    optional arguments:
      -h, --help            show this help message and exit
      -v, --version         show program's version number and exit
      -i file[,ReaderClassName], --input file[,ReaderClassName]
                            read CSR map from file
      -o file[,WriterClassName] [file[,WriterClassName] ...], --output file[,WriterClassName] [file[,WriterClassName] ...]
                            write output to file(s)
      -t file[,WriterClassName], --template file[,WriterClassName]
                            write CSR map template to file

Custom workflow
===============

Corsair can be imported to your module to enable creation of a custom workflow.

TODO
