---
icon: material/set-merge
---

# Loaders

<img src="../../assets/images/flow-loaders.drawio.svg" alt="Corsair loaders" class="invert-on-slate">


Register maps, often referred to as Control and Status Registers (CSRs), are fundamental in hardware design. They represent named memory regions where specific addresses correspond to individual registers. Each register, in turn, is composed of a collection of named bitfields. These bitfields can further define enumerated values, associating specific names with particular states or meanings. The `Register File` is a crucial input for Corsair, providing a comprehensive description of this entire hierarchy in a single, consistent format.

Corsair utilizes a system of `Loaders` to read and parse these `Register File`s. The primary role of a loader is to transform the input description, regardless of its original format, into an internal data structure known as the [`Map`](../api.md#corsair.Map) object. This [`Map`](../api.md#corsair.Map) object serves as Corsair's unified internal representation of the register map and is subsequently used by various generators to produce different outputs (like RTL code, software headers, or documentation).

Corsair aims to support a variety of input formats for register descriptions through different loaders:

*   **Serialized Data Formats:** This loader can read register descriptions from common data serialization formats such as JSON, YAML, and HJSON.
*   **Python File Loader (Coming Soon):** This will allow defining the register map directly as a Python object within a `.py` file, offering flexibility for programmatic descriptions.
*   **Text Table Loader (Coming Soon):** For those who prefer a simple, human-readable format, this loader will parse register maps from plain text tables, similar to Markdown tables.
*   **XLSX Loader (Coming Soon):** This loader will enable reading register descriptions directly from Microsoft Excel spreadsheets (`.xlsx` files).
*   **Custom User-Defined Loaders (Coming Soon):** Corsair will also provide a mechanism for users to develop and integrate their own custom loaders, allowing for support of proprietary or specialized register description formats.

The goal of each loader is consistent: to accurately interpret the source `Register File` and construct the internal [`Map`](../api.md#corsair.Map) object. This [`Map`](../api.md#corsair.Map) then acts as the single source of truth for all subsequent generation tasks.

For more detailed information on the specific syntax and structure of `Register File`s in various supported formats, please refer to the [Register File](../register-file/index.md) formats documentation.
