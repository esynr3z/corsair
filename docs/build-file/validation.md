# Validation

To ensure the correctness of your build file, you can validate it using [`corsair check`](../cli.md#corsair-check).

Additionally, a JSON schema is available to aid in editing and validation. You can access it in several ways:

* By running the command [`corsair schema build`](../cli.md#corsair-schema).
* Directly from the repository at [`schemas/corsair-build-schema.json`](https://raw.githubusercontent.com/esynr3z/corsair/refs/heads/dev2/schemas/corsair-build-schema.json).
* From the root of the documentation website at [`corsair-build-schema.json`](../corsair-build-schema.json).

If your editor supports YAML schema validation, it's definitely recommended to set it up:

=== "Visual Studio Code"

    1.  Install [`vscode-yaml`](https://marketplace.visualstudio.com/items?itemName=redhat.vscode-yaml) for YAML language support.
    2.  Add the schema under the `yaml.schemas` key in your user or
        workspace [`settings.json`](https://code.visualstudio.com/docs/getstarted/settings):

        ``` json
        {
          "yaml.schemas": {
            "https://corsair-csr.github.io/latest/corsair-build-schema.json": "*csrbuild.yaml"
          }
        }
        ```

=== "Other"

    1.  Ensure your editor of choice has support for YAML schema validation.
    2.  Add the following lines at the top of `csrbuild.yaml`:

        ``` yaml
        # yaml-language-server: $schema=https://corsair-csr.github.io/latest/corsair-build-schema.json
        ```