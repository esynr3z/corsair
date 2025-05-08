---
icon: material/set-split
---

# Generators

<img src="../../assets/images/flow-generators.drawio.svg" alt="Corsair generators" class="invert-on-slate">

Generators are a core component of Corsair, responsible for transforming the internal [`Register Model`](./register-model.md) into various output files. They act as the bridge between the abstract representation of hardware registers and the concrete artifacts needed for different stages of a project, such as RTL code, software headers, and documentation.

Each generator takes the intermediate representation of the register map as input and, according to its specific configuration, produces one or more output files. This process ensures that all outputs are consistently derived from the same validated source.

Most of Corsair's built-in generators leverage the power and flexibility of [Jinja2](https://jinja.palletsprojects.com/) templates. This templating engine allows for highly customizable output formats while maintaining a clear separation between the data (the register map) and its presentation.

The types of generators are not strictly limited. Depending on their purpose, a generator might produce a single file (e.g., a Verilog module for a register block) or multiple files (e.g., a set of C headers for different peripheral interfaces).

Conceptually, generators can be grouped into three main categories based on the type of artifacts they produce:

*   **RTL (Register Transfer Level):** These generators create artifacts necessary for hardware synthesis and simulation. Supported HDL outputs include Verilog-2001, VHDL-93, and SystemVerilog-2017.
*   **SW (Software):** This category includes generators that produce files required for software to interact with the hardware registers. These can be header files (e.g., for C/C++) or other programmatic descriptions of the register space, enabling software to access and manipulate registers.
*   **Docs (Documentation):** These generators create human-readable documentation for the register map. Outputs can range from simple text files to more structured formats like Markdown or Asciidoc, helping to keep hardware documentation synchronized with the design.

A comprehensive list of available generators, along with their specific parameters and configuration options, can be found in the [Build File - Generators](../build-file/generators/index.md) section.

**Coming Soon:** The ability to define and use custom generators declared externally, offering even greater flexibility in tailoring Corsair to a project's unique needs.
