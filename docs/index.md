# Corsair

⚠️🚨⚠️ **PROJECT'S VERSION 2.X IS UNDER ACTIVE DEVELOPMENT.** ⚠️🚨⚠️

<p align="center">
    <img src="assets/images/logo.svg" alt="logo" width="200"/>
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

Check out the [Concepts](./concepts/index.md) section to understand the core concepts of Corsair.
