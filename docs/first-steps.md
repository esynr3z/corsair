---
icon: octicons/mortar-board-16
---

# First Steps

After completing the installation as described in the [Installation guide](./installation.md), you can create a new project and build it.

You can quickly create a new project using the [`corsair init`](./cli.md#corsair-init) command:

```bash
corsair init
```

This command will create two files in the current directory: `csrmap.yaml` and `csrbuild.yaml`.

The first file, `csrmap.yaml`, describes the source CSR map. It contains the definitions of your registers and their fields. The second file, `csrbuild.yaml`, is the build file. It specifies how to process the `csrmap.yaml` and what output files (like RTL code, software headers, or documentation) should be generated.

Once you have your register map defined and the build file configured, you can generate the output files using the [`corsair build`](./cli.md#corsair-build) command:

```bash
corsair build
```

This command will process your input files according to the `csrbuild.yaml` specification and place all generated artifacts into the `corsair-build` directory by default.

To learn more about the underlying principles of Corsair, refer to the [Workflow](./concepts/workflow.md) section in our concepts guide.

For detailed information on the formats of the input files, please see the [Build File](./build-file/index.md) and [Register File](./register-file/index.md) documentation.
