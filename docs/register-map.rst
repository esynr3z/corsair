Register map
============

Array of CSRs.

## Register

Register related parameters:

| Parameter | Default | Description |
| :- | :- | :- |
| "name" | "" | Register name |
| "description" | "" | Register description |
| "address" | 0 | Register address |
| "bit_fields" | [] | Array with register bit_fields |

## Bit field

Field related parameters:

| Parameter | Default | Description |
| :- | :- | :- |
| "name" | "" | Field name. Can be omitted if only single field is present (register name will be used). |
| "description" | "" | Field description. Can be omitted if only single field is present (register description will be used).
| "initial" | 0 | Initial (reset) value for the field |
| "width" | 1 | Field width (bits) |
| "lsb" | 0 | Field LSB position |
| "access" | "rw" | Access mode for the field. One of the options below. |
| "access_flags" | False | Enable pulse generation on output "read_access" or "write_access" signals on every read or write. |
| "modifiers" | [] | Access modifiers. Choice of none or multiple options below. |

Options for "access":

| "access" | Description |
| :- | :- |
| "rw" | Read and Write access |
| "ro" | Read only |
| "wo" | Write only |

Options for "modifiers":

| "modifiers" | Description |
| :- | :- |
| "self_clear" | Write 0 - no effect, write 1 - next tick self clear. |
| "write1_to_clear" | Write 0 - no effect, write 1 - current value will be cleared. |
| "write1_to_toggle" | Write 0 - no effect, write 1 - current value will be inversed. |
| "read_to_clear" | Any CSR read - current value will be cleared. |
| "read_const" | Use "initial" as only value can be readen. |
| "external_update" | Register can be updated outside the map with some "data" bus and "update" signal. |
| "memory" | Access to memory. Read with some "data" bus, "read_enable" and "data_valid" signals. Write with some "data" bus and "write_enable" signals. |


How "modifiers" can be combined with "access":

- 'rw': 
    * no modifiers
    * 'external_update'
    * 'external_update' + 'write1_to_clear
    * 'external_update' + 'write1_to_toggle'
    * 'memory'
- 'wo':
    * no modifiers
    * 'self_clear'
    * 'memory
- 'ro':
    * no modifiers
    * 'read_const'
    * 'external_update'
    * 'external_update' + 'read_to_clear'
    * 'memory'
