---
icon: material/download
---

# Installation

Corsair is a Python package and can be installed using `pip`.

Corsair supports Python 3.10 and newer versions (including 3.11, 3.12, and 3.13).

## Basic Installation

To install the latest stable version of Corsair with its core dependencies, run the following command:

```bash
pip install corsair
```

This will install Corsair along with the following essential libraries:

*   [`jinja2`](https://pypi.org/project/Jinja2/)
*   [`pydantic`](https://pypi.org/project/pydantic/)
*   [`pyyaml`](https://pypi.org/project/PyYAML/)
*   [`typer`](https://pypi.org/project/typer/)

## Optional Features

Corsair offers optional features that can be installed based on your needs:

*   **HJSON Support**: `pip install corsair[hjson]`
    *   Enables support for HJSON register map files. Installs [`hjson`](https://pypi.org/project/hjson/).
*   **WaveDrom Support**: `pip install corsair[wavedrom]`
    *   Enables generation of WaveDrom field diagrams for your registers. Installs [`wavedrom`](https://pypi.org/project/WaveDrom/).
*   **Full Installation**: `pip install corsair[full]`
    *   Installs all available optional features.

## Installing Pre-releases

If you want to try out the latest alpha or beta versions of Corsair, you can install them by using the `--pre` flag with `pip`:

```bash
pip install --pre corsair
```

This command will install the latest pre-release version available on PyPI.
