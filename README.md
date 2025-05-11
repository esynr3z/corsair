# Corsair

⚠️🚨⚠️ **PROJECT'S VERSION 2.X IS UNDER ACTIVE DEVELOPMENT.** ⚠️🚨⚠️

<p align="center">
    <img src="docs/assets/images/logo.svg" alt="logo" width="200"/>
    <br>
    <br>
    <em>Corsair navigates you through the CSR seas.</em>
    <br>
    <em>No more mismatches between hardware, software, and documentation.</em>
    <br>
    <br>
    <em>
      <a href="https://github.com/esynr3z/corsair/actions/workflows/devcontainer.yml" target="_blank">
        <img src="https://github.com/esynr3z/corsair/actions/workflows/devcontainer.yml/badge.svg?branch=dev2" alt="Devcontainer">
      </a>
      <a href="https://github.com/esynr3z/corsair/actions/workflows/docs.yml" target="_blank">
        <img src="https://github.com/esynr3z/corsair/actions/workflows/docs.yml/badge.svg?branch=dev2" alt="Documentation">
      </a>
      <a href="https://github.com/esynr3z/corsair/actions/workflows/tests.yml" target="_blank">
        <img src="https://github.com/esynr3z/corsair/actions/workflows/tests.yml/badge.svg?branch=dev2" alt="Tests & Checks">
      </a>
    </em>
</p>

<h4 align="center">
  <a href="https://corsair-csr.github.io">Documentation</a> |
  <a href="https://github.com/esynr3z/corsair">Repository</a>
</h4>

**Corsair** is a CLI tool and Python library designed to define and manage Control and Status Register (CSR) maps for HDL projects. It generates code and documentation from a single CSR description file, effectively eliminating any mismatches between different representations of registers.

## Features

*   **Single Source of Truth:** Define CSR maps in a single file (e.g., YAML, JSON) and generate various outputs from it.
*   **Code Generation:** Automatically generate HDL, software sources, and documentation from the CSR map.
*   **CLI and API:** Offers both a command-line interface for quick operations and a Python API for more complex, custom workflows.
*   **Customizable Workflows:** Supports user-side extensions for attributes, configurations, templates, and input/output formats.

Check out the [Concepts](https://corsair-csr.github.io/latest/concepts/) section to understand the core concepts of Corsair.

## Quick Start

To install Corsair, use pip:

```bash
pip install corsair
```

Corsair requires Python 3.10 to 3.13. By default, only core dependencies are installed. To include all features, install with the `[all]` extra:

```bash
pip install corsair[all]
```

For detailed installation instructions and information about optional features, see the [Installation Guide](https://corsair-csr.github.io/latest/installation/).

Then you can quickly create a new project using the [`corsair init`](https://corsair-csr.github.io/latest/cli/#corsair-init) command:

```bash
corsair init
```

This command will create two files in the current directory: `csrmap.yaml` and `csrbuild.yaml`.

The first file, `csrmap.yaml`, describes the source CSR map. It contains the definitions of your registers and their fields. The second file, `csrbuild.yaml`, is the build file. It specifies how to process the `csrmap.yaml` and what output files (like RTL code, software headers, or documentation) should be generated.

Once you have your register map defined and the build file configured, you can generate the output files using the [`corsair build`](https://corsair-csr.github.io/latest/cli#corsair-build) command:

```bash
corsair build
```

This command will process your input files according to the `csrbuild.yaml` specification and place all generated artifacts into the `corsair-build` directory by default.

To learn more about the underlying principles of Corsair, refer to the [Workflow](https://corsair-csr.github.io/latest/concepts/workflow) section in our concepts guide.

For detailed information on the formats of the input files, please see the [Build File](https://corsair-csr.github.io/latest/build-file/) and [Register File](https://corsair-csr.github.io/latest/register-file/) documentation.


## Development

Please follow the [Contributing Guide](CONTRIBUTING.md).

All changes are documented in the [Changelog](CHANGELOG.md).

## License

Corsair is licensed under [MIT License](LICENSE.txt).
