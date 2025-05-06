---
icon: octicons/workflow-16
---

# Workflow



<img src="../../assets/images/flow.drawio.svg" alt="Corsair flow" class="invert-on-slate">

The Corsair transforms register descriptions into various output files like RTL code, software headers, and documentation. This process ensures consistency across different project aspects.

The workflow consists of the following stages:

1.  **Inputs:**
    *   `Register File`: Contains the definitions of registers and bitfields (e.g., in YAML or JSON format).
    *   `Build File`: Recipe that describes how to load the register file and transform it into various outputs.

2.  **Parsing & Validation:**
    *   `Loaders`: Read and parse the `Register File` based on its format. Corsair supports multiple formats via different loaders.
    *   `Configuration`: Processes the `Build File` to guide the loading and generation steps.
    *   Input data and build specification are validated during this stage.

3.  **Internal Representation:**
    *   `Register Model`: A unified, internal data structure representing the parsed and validated register map. This model serves as the single source of truth for the generation stage.

4.  **Generation:**
    *   `Generators`: Use the `Register Model` and `Configuration` data to create the final output files. Different generators produce different types of outputs (e.g., Verilog, VHDL, C headers, Markdown).

5.  **Outputs:**
    *   `RTL`: Hardware description language files for synthesis or simulation.
    *   `SW`: Software files, such as headers or drivers, for interacting with the registers.
    *   `Docs`: Documentation files describing the register map.

This structured flow ensures that all outputs are generated consistently from the same validated source description, guided by the project's configuration.

For example, if a build file (e.g. `csrbuild.yaml`) is present in the current directory, running:

```bash
corsair build
```

will generate all output artifacts in the created `corsair-build` directory. For more details on the `build` command, see the [CLI documentation](../cli.md#corsair-build).
