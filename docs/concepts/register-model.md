---
icon: material/layers-outline
---

# Register Model

<img src="../../assets/images/flow-register-model.drawio.svg" alt="Corsair register model" class="invert-on-slate">

The Register Model is a cornerstone of the Corsair workflow, acting as the standardized internal representation of hardware's register map. As detailed in the [Workflow description](./workflow.md), this model is constructed from input files and serves as the definitive source for all output generation processes, ensuring consistency across documentation, RTL code, and software headers.

This model provides a structured way to define all the components of a register map.

**Basic Structure**

In its simplest form, the Register Model describes a hierarchy of elements:

*   **[`Map`](../api.md#corsair.Map)**: This is the top-level object, representing an address map. It contains other mappable elements.
*   **[`Register`](../api.md#corsair.Register)**: Contained within a [`Map`](../api.md#corsair.Map), [`Register`](../api.md#corsair.Register) objects represent individual hardware registers, each with its own address and properties.
*   **[`Field`](../api.md#corsair.Field)**: Each [`Register`](../api.md#corsair.Register) is composed of one or more [`Field`](../api.md#corsair.Field) objects. A [`Field`](../api.md#corsair.Field) defines a specific group of bits within the register, its access type, reset value, and other characteristics.
*   **[`Enum`](../api.md#corsair.Enum)**: A [`Field`](../api.md#corsair.Field) can optionally have an associated [`Enum`](../api.md#corsair.Enum) (enumeration). This allows you to define meaningful names for specific values that the field can take.
*   **[`EnumMember`](../api.md#corsair.EnumMember)**: Each [`Enum`](../api.md#corsair.Enum) consists of several [`EnumMember`](../api.md#corsair.EnumMember) items, where each member defines a specific value and its corresponding name or description.

This hierarchical structure allows for a clear and organized representation of most common register layouts.

**Advanced Features (Coming Soon)**

To handle more intricate and complex hardware designs, Corsair plans to extend the Register Model with the following advanced features. Please note that these are currently under development ("coming soon"):

*   **Sub-[`Map`](../api.md#corsair.Map)**: A [`Map`](../api.md#corsair.Map) object nested within another [`Map`](../api.md#corsair.Map). This is useful for grouping registers into distinct sub-regions or blocks within a larger address space.
*   **[`MapArray`](../api.md#corsair.MapArray)**: An array of [`Map`](../api.md#corsair.Map) objects. This allows for the definition of repeating groups of registers where each group has the same internal structure and properties but resides at a different base address or has a unique index.
*   **[`RegisterArray`](../api.md#corsair.RegisterArray)**: An array of [`Register`](../api.md#corsair.Register) objects within a [`Map`](../api.md#corsair.Map). This is used to describe a series of identical registers that share the same definition and properties but are differentiated by their indices and address offsets.
*   **[`Memory`](../api.md#corsair.Memory)**: Represents a block of memory within a [`Map`](../api.md#corsair.Map). This is used to indicate that a range of addresses is mapped to a memory resource rather than individual registers.
*   **[`MemoryArray`](../api.md#corsair.MemoryArray)**: An array of [`Memory`](../api.md#corsair.Memory) regions. This allows for describing multiple identical memory blocks, each with its own index and address offset.
*   **[`FieldArray`](../api.md#corsair.FieldArray)**: An array of [`Field`](../api.md#corsair.Field) objects within a [`Register`](../api.md#corsair.Register). This feature is for defining repeating fields that share the same description and properties but have different bit offsets or indices within the register.

This chapter serves as an introduction to the concept and structure of the Register Model. For details on how this model is populated from specific input file formats or how it's utilized by different code generators, please refer to their respective documentation sections:

*   [Register File](./register-file/index.md)
*   [Build File](./build-file/index.md)
