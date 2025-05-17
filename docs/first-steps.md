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

=== "csrmap.yaml"

    ``` yaml
    # Root of a register map
    name: uart
    doc: UART register map
    address_width: 12
    register_width: 32
    offset: 0
    items: # Map consists of addressable items (e.g. registers)
    - kind: register
      name: ctrl
      doc: Control register
      offset: 0x10
      fields: # Register consists of fields
      - name: baud
        doc: Baudrate value
        offset: 0
        reset: 0
        width: 2
        access: rw
        hardware: o
        enum: # Field may contain an enumeration
          name: baud_enum
          doc: Baudrate enumeration
          members:
          - name: b9600
            doc: 9600 baud
            value: 0
          - name: b38400
            doc: 38400 baud
            value: 1
          - name: b115200
            doc: 115200 baud
            value: 2
    ```

=== "csrbuild.yaml"

    ``` yaml
    # How to load the input file
    loader:
      kind: yaml
      mapfile: csrmap.yaml

    # How to generate the output files
    generators:
      doc_markdown: # Arbitrary label for a generation target
        kind: markdown
        file_name: regmap.md
        image_dir: img
        show_images: true
        title: Register Map
        wavedrom:
          bits: 8
    ```



The first file, `csrmap.yaml`, describes the source CSR map. It contains the definitions of your registers and their fields. The second file, `csrbuild.yaml`, is the build file. It specifies how to process the `csrmap.yaml` and what output files (like RTL code, software headers, or documentation) should be generated.

Once you have your register map defined and the build file configured, you can generate the output files using the [`corsair build`](./cli.md#corsair-build) command:

```bash
corsair build
```

This command will process your input files according to the `csrbuild.yaml` specification and place all generated artifacts into the `corsair-build` directory by default:

``` bash
$ corsair build
INFO     Output directory: /home/corsair/corsair-build
INFO     Read build specification
INFO     Targets to build: ['doc_markdown']
INFO     Load CSR map
INFO     Generate outputs for 'doc_markdown'
INFO     /home/corsair/corsair-build/doc_markdown/regmap.md
INFO     /home/corsair/corsair-build/doc_markdown/img/uart_ctrl.svg
INFO     Build completed successfully
```

To learn more about the underlying principles of Corsair, refer to the [Workflow](./concepts/workflow.md) section in our concepts guide.

For detailed information on the formats of the input files, please see the [Build File](./build-file/index.md) and [Register File](./register-file/index.md) documentation.
