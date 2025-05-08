---
icon: octicons/tools-16
---

# Build Specification

<img src="../../assets/images/flow-build-specification.drawio.svg" alt="Corsair build
specification" class="invert-on-slate">

Corsair is a configuration-file-oriented tool. This means that all the necessary details for the generation process are conveyed through a dedicated file. This file, often referred to as the build file, build specification, build script, or build recipe, encapsulates all the essential information for a build. It dictates which register map to use, which loader should parse it, the specific settings for that loader, and defines the available generation targets along with their configurations. You can think of it as a Makefile specifically for Corsair.

The build file and the register map descriptions are intentionally kept separate. This decoupling enhances reusability and simplifies the management of different build configurations.

The build file uses the YAML format. To aid in editing and ensure correctness, a [JSON schema](https://json-schema.org/) is available (you can generate it using the [`corsair schema`](../cli.md#corsair-schema)). Additionally, Corsair itself can validate the build file (using the [`corsair check`](../cli.md#corsair-check) command).

The build process is initiated with the [`corsair build`](../cli.md#corsair-build) command. During this process, the build file is first validated and parsed into a [`BuildSpecification`](../api.md#corsair.BuildSpecification) object. This configuration object is then used to appropriately set up and configure the necessary loader for the register map and the generators for the output targets.

For a more in-depth understanding of the build file, its structure, and specific features, please refer to the dedicated [Build File](../build-file/index.md) section.
