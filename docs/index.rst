===================================
Corsair
===================================

.. image:: logo.svg
    :width: 128px
    :alt: Corsair logo
    :align: center



Corsair is a tool that makes it easy to organize and support control and status register (CSR) map for an any FPGA/ASIC project.
You just need to create and fill single CSR map description file once and then generate HDL code, headers, documentation and etc.

Instal the latest stable version from pypi:

::

    python3 -m pip install -U corsair

Architecture of the tool is quite straightforfard and follows the "one to many" principle. So that you need to support only the one input file to generate unlimited number of output artifacts. This effectively eliminates any syncroniztion issues between outputs, e.g. documentation and HDL code will always match each other since the only one common source is used.

.. image:: arch.svg
    :alt: Corsair architecture
    :align: center

Please follow to :ref:`Workflow <workflow>` and :ref:`CSR description file <csr-map>` parts to figure out how Corsair works.

.. toctree::
   :maxdepth: 2
   :caption: Basics

   workflow.rst
   csr-map.rst

.. toctree::
   :maxdepth: 2
   :caption: Buses and bridges

   local-bus.rst
   apb2lb.rst
   axil2lb.rst
   amm2lb.rst
   spi2lb.rst

.. toctree::
   :maxdepth: 2
   :caption: API

   config-api.rst
   regmap-api.rst
   readers-api.rst
   writers-api.rst

.. toctree::
   :maxdepth: 2
   :caption: Additional materials

   contributing.rst
   changelog.rst

:ref:`Keyword Index <genindex>`
