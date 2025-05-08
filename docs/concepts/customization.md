---
icon: octicons/sliders-16
---

# Customization

<img src="../../assets/images/flow-customization.drawio.svg" alt="Corsair customization" class="invert-on-slate">

Corsair is designed with end-to-end extensibility in mind, offering the flexibility to adapt to the specific needs of any project. This adaptability is achieved through several key mechanisms:

*   **Register File Customization**: Every named item within the register file (such as maps, registers, and fields) includes a [`metadata`](../api.md#corsair.NamedItem.metadata) field. This field allows for the inclusion of free-form parameters. These parameters can then be utilized by generators or within Jinja2 templates to tailor the output.

*   **Build File and Generator Configuration**:
    *   The configuration for generators in the build file can be extended using an [`extra`](../api.md#corsair.GeneratorConfig.extra) field. This allows for the definition of additional options that can be accessed within templates, providing further control over the generation process.
    *   Furthermore, all generators permit the overriding of their default templates. This enables users to substitute standard templates with their own custom versions, seamlessly integrating user-specific logic into existing generators.

*   **Plugin System for Loaders and Generators (Coming Soon)**: Users will be able to introduce their own custom loaders and generators. This can be achieved either through a plugin system or by directly providing Python files, offering powerful extensibility for input processing and output generation.

These customization options ensure that Corsair can be finely tuned to integrate smoothly into diverse project workflows and meet unique requirements. For more detailed information on specific customization points, please refer to the relevant sections on register files, build files, and the plugin system (once available).
