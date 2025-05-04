---
icon: material/head-lightbulb-outline
---

# Philosophy

Creating and maintaining a CSR map in any HDL project is a tedious task. Additionally, register information exists simultaneously across different abstraction layers:

- Hardware
- Software
- Documentation

It is easy to make mistakes and lose consistency between these layers. While automation can help address this issue, the unique nature of HDL project workflows often leads to ad hoc solutions.

## The Goal

**The primary goal of this project is to provide a CSR management tool that generates a consistent set of artifacts for various purposes from a single register map description. The tool is designed to be flexible enough to integrate into ANY workflow.**

## Core Principles

The project's architecture and technical solutions are built on the following principles:

1. **Single source of truth**.
Generate all artifacts from a single meta-description of the register model.

2. **Low barrier to entry**.
Typical EDA tools are often cryptic and sometimes even hostile to inexperienced users. Users should be able to get started quickly by reading a short README and running a few commands.

3. **Automation first**.
Use formats that are both human- and machine-readable for input and intermediate data. Provide schemas, organize output files predictably, and offer CLI options for fine-tuning.

4. **Customizable workflows**.
Allow seamless user-side extensions for attributes, configurations, templates, and input/output formats. Provide a fully-featured API to enable creating unique workflows from scratch.

5. **Validate everything**.
Mistakes can have significant consequences. Validate all input data thoroughly at runtime. Test and lint rigorously all potential outputs during development.

6. **Usability matters**.
Provide autocompletion wherever possible. Always require the minimum necessary input from the user, inferring the rest or filling in with reasonable defaults.

7. **Output Neutrality**.
Treat all potential output artifacts—be it HDL, documentation, or others—as first-class citizens. Design the tool to be inherently flexible, without built-in biases towards specific output types or formats.
