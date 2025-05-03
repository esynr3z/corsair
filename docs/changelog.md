---
icon: octicons/versions-16
---

# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- Reorganize code for better decomposition, encapsulation, stricter API and easier maintenance and development
- Start using [pydantic](https://pypi.org/project/pydantic/) for all internal data models
- Reorganize CLI into commands via [typer](https://pypi.org/project/typer/)
- Switch to YAML for a build specification (former csrconfig) ([#81](https://github.com/esynr3z/corsair/issues/81))
- Switch to modern python infrastructure for linting and package management ([uv](https://pypi.org/project/uv/), [ruff](https://pypi.org/project/ruff/), [pyright](https://pypi.org/project/pyright/))
- Rework CI to run jobs inside [devcontainer](https://containers.dev/)
- Switch to [MkDocks-Material](https://github.com/squidfunk/mkdocs-material) for documentation rendering
- Switch to [Github Pages](https://pages.github.com/) for documentation hosting
- Start following [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) specification for commit messages
- Start following [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) specification for changelog ([#82](https://github.com/esynr3z/corsair/issues/82))

### Added

- Git pre-commit hooks via [pre-commit](https://pre-commit.com/) tool
- Docker image with development workspace including Verilator and Modelsim
- Devcontainer config to facilitate workspace deployment and IDE use
- Cursor rules to facilitate using of LLMs via [Cursor](https://www.cursor.com/)
- Package features management to avoid installing unnecessary dependencies (e.g. hjson, wavedrom)
- CLI command `corsair check` to validate input files
- CLI command `corsair schema`  to generate JSON-schemas of input files for IDE hints, autocompletion and validation
- CLI command `corsair build`  to render outputs
- `BuildSpecification` data model to store build targets and configuration
- Register map data models (`Map`, `Register`, `Field`, `Enum`, `EnumMember`) for internal CSR representation
- `SetializedParser` to parse register map from JSON/YAML/HJSON files
- `WavedromGenerator` to generate SVG images of bitfields
- `MarkdownGenerator` to generate Markdown document for a register map

### Removed

- Corsair 1.x source code, documentation, examples

## [1.0.4] - 2023-03-17

### Fixed

- `rolh`/`roll` missing latch bug.
- Constants comparison on address in VHDL.
- C/C++ header generation.

## [1.0.3] - 2023-03-06

### Fixed

- Various bug fixes.

## [1.0.2] - 2021-09-26

### Fixed

- Overlapping of bitfield names in rendered images for registers.

## [1.0.1] - 2021-09-08

### Fixed

- Issue where the input `globconfig` file was not being applied to generators.

## [1.0.0] - 2021-09-03

### Added

- New configuration file format (INI).
- New file generation flow.
- Enums.
- C header generator.
- Verilog header generator.
- SystemVerilog package generator.
- Bus interface embedding (AXI-Lite, APB, Avalon-MM) into a register map.
- VHDL register map generator.
- Plenty of examples.

### Changed

- **Reworking the entire project almost from scratch. Lots of breaking changes.**
- Refactoring of all core modules.
- Rework of documentation.
- Update the tests.
- Many minor tweaks and fixes.

## [0.3.0] - 2021-02-21

### Added

- 'Reserved' bitfields to Markdown.
- `access_strobes` attribute for register.
- Complementary registers.
- `write_lock` attribute for register.
- FIFO bitfield modifier.
- AXI-Lite to Local Bus bridge on Verilog.
- Avalon-MM to Local Bus bridge on Verilog.

### Fixed

- Markdown table row endings.
- Installation guides.

## [0.2.0] - 2021-01-08

### Added

- Verilog and Markdown writers for a register map.
- Local Bus bridge writer.
- APB to Local Bus bridge on Verilog.
- HDL testing environment.
- CI/CD via Github Actions.
### Changed
- Rework CLI keys.
- Documentation fixes, code prettifying and etc.

### Fixed

- Entry point for CLI.

## [0.1.0] - 2020-12-16

### Added

- Setup repository.
- Setup documentation.
- Setup testing.
- Implementation of core classes.
- Support for running from a command line.
- JSON and YAML readers.
- JSON and YAML writers.
