# Build File Reference

The Corsair build file is a YAML formatted file that defines all the necessary details for the generation process.

* For a higher-level overview of its role, refer to the [Build Specification](../concepts/build-specification.md) concept.
* You can initialize a new build file using the [`corsair init`](../cli.md#corsair-init) command.

By default, the build file is named `csrbuild.yaml`.

## File Structure

```yaml
# What register map to load and how to load it
loader:
  kind: yaml # select the loader type (mandatory)
  mapfile: csrmap.yaml # path to the register map file
  # ... other loader-specific options

# What to generate: map of targets with unique names
generators:
  # Target example: generate markdown artifacts
  my_markdown_target:
    kind: markdown # select the generator type (mandatory)
    # ... other generator-specific options

  another_target:
    # ... target kind and its specific options
```

## Global Keywords

Global keywords control the overall behavior of the build process.

| Keyword | Default | Description |
| --- | --- | --- |
| [`loader`](#loader) | [Default YAML loader](#yaml-loader) | Selects and configures the loader to use. |
| [`generators`](#generators) | - | Definition of all the generation targets. |

### `loader`

This keyword specifies the configuration for the component responsible for parsing the register map description.

**Supported values**: An object defining the configuration for the loader. Object key `kind` is mandatory and defines the type of loader to use. Other options are loader-specific.

**Example** of using the `yaml` loader with all default options:
```yaml
loader:
  kind: yaml
  # ... other loader-specific options
```

**Related topics**:

- [Loaders concept](../concepts/loaders.md)
- [Loaders reference](#loaders)

### `generators`

This keyword specifies all the generation targets (i.e. selects and configures all the output generators).

**Supported values**: A dictionary where each key is a unique name for a generator instance and the value is an object configuring that specific generator.

**Example** of using several `markdown` generators with some options:
```yaml
generators:
  markdown_with_images:
    kind: markdown
    show_images: True
  markdown_without_images:
    kind: markdown
    show_images: False
```

**Additional details**: This section defines one or more output generators. Each generator entry must have a unique name and specify its type (which dictates the available configuration options for that generator) and other generator-specific settings. This field must contain at least one generator configuration.

**Related topics**:

- [Generators concept](../concepts/generators.md)
- [Generators reference](#generators_1)

## Loaders

An object (dictionary) under the [`loader`](#loader) keyword.

| Name | Kind | Description |
| --- | --- | --- |
| [YAML Loader](#yaml-loader) | `yaml` | Loads the register map from a YAML file. |
| [JSON Loader](#json-loader) | `json` | Loads the register map from a JSON file. |
| [HJSON Loader](#hjson-loader) | `hjson` | Loads the register map from a HJSON file. |

### YAML Loader

### JSON Loader

### HJSON Loader

## Generators

### Markdown Docs
