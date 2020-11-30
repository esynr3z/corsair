# Configuration options

Collection of global parameters. These parameters can be used in special section of a CSR description file.

Any of groups/parameters with default values can be skipped.

## read_filler

Value to be returned if read of empty address or WO register is performed.

**Default value**: "0x0".

## address_calculation

Group of address calculation related parameters.

| Parameter | Default | Description |
| :- | :- | :- |
| "auto_increment_mode" | "none" | Address auto increment mode, if no address is provided for a register  |
| "auto_increment_value" | 4 | Auto increment with provided value: 1 - 1 byte, 4 - 4 bytes, etc.  |
| "alignment_mode" | "data_width" | Check for address alignment |
| "alignment_value" | 4 | Address alignment with provided value: 1 - 1 byte, 4 - 4 bytes, etc. |

Options for "auto_increment_mode":

| "auto_increment_mode" | Description |
| :- | :- |
| "none" | No address auto increment. If no address is provided, error will be generated.  |
| "data_width" | Enable auto increment with value based on "data_width" of "interface_generic" group |

Options for "alignment_mode":

| "alignment_mode" | Description |
| :- | :- |
| "none" | No check of address alignment  |
| "data_width" | Enable check of address alignment based on "data_width" of "interface_generic" group |

## register_reset

Type of a reset being used.

Choice of:

| "register_reset" | Description |
| :- | :- |
| "sync_pos" | Synchronous active high reset |
| "sync_neg" | Synchronous active low reset |
| "async_pos" | Asynchronous active high reset |
| "async_neg" | Asynchronous active low reset |
| "init_only" | No register reset. Declaration with initialization will be used. |

**Default value**: "sync_pos".

## interface_generic

Group of generic interface related parameters.

| Parameter | Default | Description |
| :- | :- | :- |
| "type" | "lb" | Interface type. One of the options below. |
| "data_width" | 32 | Data bus bit width |
| "address_width" | 32 | Address bus bit width |

Options for "type":

| "type" | Description |
| :- | :- |
| "amm" | Avalon-MM interface |
| "apb" | APB4 interface |
| "axil" | AXI4-Lite interface |
| "lb"  | Local Bus interface |

*Note*: more details about Local Bus interface can be found in [specification](local_bus.md).

Allowed combinations of the parameters:

| "type" | "data_width" | "address_width" |
|:-|:-|:-|
| "amm" | 8, 16, ..., 1024 (power of 2) | 1 - 64 |
| "apb" | 8, 16, 32 | 1 - 32 |
| "axil" | 32, 64 | 32, 64|
| "lb" | 8, 16, ... (any power of 2) | 1 - 64 |

## interface_specific

Group of interface type specific parameters. This block is unque for every interface type.
