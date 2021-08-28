# Corsair

![corsair_logo](docs/img/logo.png)

[![Documentation Status](https://readthedocs.org/projects/corsair/badge/?version=latest)](https://corsair.readthedocs.io/en/latest/?badge=latest)
![PyTest Status](https://github.com/esynr3z/corsair/workflows/pytest/badge.svg)
[![PyPI version](https://badge.fury.io/py/corsair.svg)](https://badge.fury.io/py/corsair)


Corsair is a tool that makes it easy to create and maintain control and status register (CSR) map for any HDL project. It allows you to describe your register map in a single file and then generate HDL code, headers, documentation and other things. This effectively eliminates any mismatches between hardware, software and documentation of your IP-core.

![corsair_flow](docs/img/corsair_flow.png)

## Features

- Various human-readable input formats: JSON, YAML or plain text table
- HDL code generation: Verilog module with register map, Verilog header or SystemVerilog package with parameters and definitions
- Multi-protocol support: APB, AXI-Lite, Avalon-MM
- Documentation generation in Markdown
- Generation of software-related files: C header, Python module
- Extensibility: support of external file generators
- API: creation of custom workflow with corsair API

Corsair documentation is on the [ReadTheDocs.io](https://corsair.readthedocs.io).

## Install

Depending on your system, Python 3 executable might be `python` or `python3`.
If there any permissions issues, add `--user` key to the installation scripts.

To install the latest stable release:

```sh
python3 -m pip install -U corsair
```

## Quick start

Register map consists of a set of memory mapped registers (also referred as CSRs), and registers are made up of bit fields. To know more about registers, bit fields and their attributes please check the [Register map](https://corsair.readthedocs.io/en/latest/regmap.html) documentation page.

You can create a template for a register map in a format you like (choose onе from `json`, `yaml`, `txt`) :

```sh
corsair -t yaml
```

This creates two files: one for register map in the format specified `regs.yaml`, and other for configuration - `csrconfig`.

Corsair is configuration-file-oriented tool. By default, it uses INI configuration file `csrconfig`. It specifies all the things needed for generation - input register map file, global parameters and output files (also called targets). Check the [Configuration file](https://corsair.readthedocs.io/en/latest/config.html) page to get more details about `csrconfig` and the [Introduction](https://corsair.readthedocs.io/en/latest/introduction.html) page to get general information about workflow.

`csrconfig` for corsair is as like as `Makefile` for make, or `CMakeLists.txt` for cmake. It acts like build script and it works in the similar way, just run in the directory with `csrconfig` file:

```sh
corsair
```

And then all the magic happens.

There are some additional options for overriding working directory, register map or configuration file - to get help simply run

```sh
corsair -h
```

If you looking for some more examples please check `examples` folder.

## Development

Please follow the [Developer's Guide](https://corsair.readthedocs.io/en/latest/contributing.html).

## License

Corsair is licensed under [MIT License](LICENSE.txt).
