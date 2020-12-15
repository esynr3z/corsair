============
Contributing
============

Installation
------------

You can install the latest development version from GitHub:

::

    python3 -m pip install -U git+https://github.com/esynr3z/corsair.git

You can clone GitHub repository and run application from the project root:

::

    git clone https://github.com/esynr3z/corsair.git
    cd corsair
    python3 -m corsair --help


Code style
----------

`PEP 8 Speaks <https://github.com/OrkoHunter/pep8speaks/>`_ is added to automatically review Python code style over Pull Requests.

Linter settings:

* Linter: pycodestyle
* Max line length: 120
* Errors and warnings to ignore: W504, E402, E731, C406, E741

Testing
-------

Install PyTest:

::

    python3 -m pip install -U pytest

Run tests from the root folder:

::

    pytest -v

Documentation
-------------

Install Sphinx and extensions:

::

    python3 -m pip install -U sphinx sphinx_rtd_theme m2r2

Run from ``docs`` folder to build the documentation and test docstrings:

::

    make clean html doctest
