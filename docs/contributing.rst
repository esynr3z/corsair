=================
Developer's guide
=================

Installation
============

.. note::
    Depending on your system, Python executable might be ``python`` or ``python3``.
    If there any permissions issues, add ``--user`` key to the installation scripts.

Install dependencies first:

::

    python3 -m pip install gitpython pyyaml jinja2 wavedrom

Then clone GitHub repository and you'll be able to run application from the project root:

::

    git clone https://github.com/esynr3z/corsair.git
    cd corsair
    python3 -m corsair --help

Or install it:

::

    python3 setup.py install


Code style
==========

`PEP 8 Speaks <https://github.com/OrkoHunter/pep8speaks/>`_ is added to automatically review Python code style over Pull Requests.

Linter settings:

* Linter: pycodestyle
* Max line length: 120
* Errors and warnings to ignore: W504, E402, E731, C406, E741

You can also install `PEP8 Git Commit Hook <https://gist.github.com/esynr3z/206e164023a794eb0c96d827de31bd49>`_ and code style will be checked before any commit.

Testing
=======

Install PyTest:

::

    python3 -m pip install -U pytest pytest-xdist

HDL tests use Modelsim, so make sure that Modelsim is installed and visible in PATH.


Run tests from the root folder on all available cores:

::

    pytest -v -n auto

Run tests for docstrings:

::

    pytest --doctest-modules corsair

Documentation
=============

Install Sphinx and extensions:

::

    python3 -m pip install -r docs/requirements.txt

Run from ``docs`` folder to build the documentation:

::

    make clean html
