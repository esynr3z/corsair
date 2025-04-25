# Schemas

This directory contains the JSON schema files used by the Corsair tool.

Schemas can be used for autocomplete and validation of data in all main serializable formats, e.g. YAML, JSON, TOML, etc.

*   **`corsair-build-schema.json`**: JSON schema for the Corsair build configuration file (`csrbuild.yaml`).
*   **`corsair-map-schema.json`**: JSON schema for the Corsair register map definition files (typically `csrmap.yaml` files).
*   **`generate.sh`**: A shell script used to regenerate the schema files based on the current Corsair models.

## Usage

### VSCode: YAML files

- Install [vscode-yaml](https://marketplace.visualstudio.com/items?itemName=redhat.vscode-yaml) for YAML language support.
- Add the schema under the `yaml.schemas` key in your user or workspace `settings.json`:

```json
{
  "yaml.schemas": {
    "https://raw.githubusercontent.com/esynr3z/corsair/refs/heads/dev2/schemas/corsair-build-schema.json": "*csrbuild.yaml",
    "https://raw.githubusercontent.com/esynr3z/corsair/refs/heads/dev2/schemas/corsair-map-schema.json": "*csrmap.yaml",
  },
}
```

### VSCode: JSON files

Add the schema under the `json.schemas` key in your user or workspace `settings.json`:

```json
{
  "json.schemas": [
    {
      "fileMatch": [
        "*csrmap.json"
      ],
      "url": "https://raw.githubusercontent.com/esynr3z/corsair/refs/heads/dev2/schemas/corsair-map-schema.json"
    }
  ]
}
```

### Other: YAML files

- Ensure your editor has support for YAML schema validation.
- Add the following lines at the top of `csrmap.yaml`:

```yaml
# yaml-language-server: $schema=https://raw.githubusercontent.com/esynr3z/corsair/refs/heads/dev2/schemas/corsair-map-schema.json
```

- Add the following lines at the top of `csrbuild.yaml`:

```yaml
# yaml-language-server: $schema=https://raw.githubusercontent.com/esynr3z/corsair/refs/heads/dev2/schemas/corsair-build-schema.json
```

## Updating Schemas

The JSON schema files are automatically generated based on the Pydantic models defined within the Corsair source code.

To update the schemas manually, run the `generate.sh` script.
