---
icon: material/check-outline
---

# File Confidence

<img src="../../assets/images/flow-file-confidence.drawio.svg" alt="Corsair file confidence" class="invert-on-slate">

Ensuring the integrity of all input and output files is a core aspect of Corsair, directly reflecting the "Validate everything" principle outlined in our [philosophy](./philosophy.md). This section provides an overview of how Corsair handles file validation, helping you understand te built-in checks and how to leverage them.

## Input File Validation

Corsair primarily deals with two types of input files: the `Build file` and the `Register file`. Both are crucial for the correct generation of your desired outputs.

### Build File

The `Build file` (e.g., `csrbuild.yaml`) contains the recipe that describes how to load your register descriptions and transform them into various outputs.

*   **Automatic Validation**: When Corsair parses a `Build file`, it's validated against a [Pydantic](https://docs.pydantic.dev/) model. This ensures the structure and data types conform to the expected schema.
*   **Manual Validation**: You can manually check the integrity of your `Build file` using the `corsair check` command. For more details, refer to the [CLI documentation](../cli.md#corsair-check).
*   **Schema-based Validation**: For integration with external validators or for a deeper understanding of the expected structure, Corsair provides a JSON schema for the `Build file`. You can:
    *   Generate it using the `corsair schema` command (see [CLI documentation](../cli.md#corsair-schema)).
    *   Find it in the [Corsair repository](https://github.com/esynr3z/corsair/blob/dev2/schemas/corsair-build-schema.json).
    *   Access it on the [documentation site](../corsair-build-schema.json).

### Register File

The `Register file` (e.g., in YAML or JSON format) contains the actual definitions of your registers and bitfields.

*   **Automatic Validation**: Similar to the `Build file`, the `Register file` is validated against a [Pydantic](https://docs.pydantic.dev/) model during the parsing stage.
*   **Manual Validation**: You can manually check your `Register file` using the `corsair check` command (see [CLI documentation](../cli.md#corsair-check)).
*   **Schema-based Validation**: A JSON schema is also available for the `Register file` to facilitate validation with other tools. You can:
    *   Generate it using the `corsair schema map` command (see [CLI documentation](../cli.md#corsair-schema)).
    *   Find it in the [Corsair repository](https://github.com/esynr3z/corsair/blob/dev2/schemas/corsair-map-schema.json).
    *   Access it on the [documentation site](../corsair-map-schema.json).

## Output File Validation (Coming Soon)

Corsair aims to produce clean and error-free output files. The validation strategies for generated outputs are currently under development and will include:

*   **HDL Outputs**: Generated HDL files (e.g., Verilog, VHDL) will be tested using strict compilation options to ensure they are lint-free and warning-free.
*   **Documentation Outputs**: Linters will be employed during testing to verify the cleanliness and correctness of generated documentation files.
*   **Software Outputs**: Similarly, linters will be used to check the generated software files (e.g., C headers) for quality and correctness.

This multi-layered validation approach ensures that from input to output, Corsair maintains a high level of confidence in the files it processes and produces, contributing to a more robust and reliable workflow.
