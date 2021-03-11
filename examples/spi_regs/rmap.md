# rmap

Created with [Corsair](https://github.com/esynr3z/corsair) vgit-latest.

Register map v1.0.

## Conventions

| Name  | Type     | Description |
| :---  | :---     | :---        |
| rw    | access   | Read or Write |
| ro    | access   | Read Only. Write has no effect. |
| wo    | access   | Write Only. Zeros are read. |
| sc    | modifier | Self Clear. Write 0 - no effect, write 1 - next tick self clear. |
| w1tc  | modifier | Write 1 To Clear. Write 0 - no effect, write 1 - current value will be cleared (all zeros). |
| w1ts  | modifier | Write 1 To Set. Write 0 - no effect, write 1 - current value will be set (all ones). |
| w1tt  | modifier | Write 1 To Toggle. Write 0 - no effect, write 1 - current value will be inversed. |
| rtc   | modifier | Read To Clear. Current value will be cleared next tick after read. |
| const | modifier | Constant. Reset value is hardcoded as only value can be read. |
| hwu   | modifier | Hardware Update. Register value can be updated from outside the map with hardware. |

## Register map

| Name                     | Address    | Description |
| :---                     | :---       | :---        |
| [LEDCTRL](#ledctrl)      | 0x00       | LED control register | |
| [RDFIFO](#rdfifo)        | 0x04       | Read FIFO | |

## LEDCTRL

LED control register

Address offset: 0x00

Reset value: 0x0000

![](rmap_img/ledctrl.svg)

| Name             | Bits   | Mode            | Reset      | Description |
| :---             | :---   | :---            | :---       | :---        |
| -                | 15:9   | -               | 0x0        | Reserved |
| BEN              | 8      | rw              | 0x0        | Enable blue led |
| -                | 7:5    | -               | 0x0        | Reserved |
| GEN              | 4      | rw              | 0x0        | Enable green led |
| -                | 3:1    | -               | 0x0        | Reserved |
| REN              | 0      | rw              | 0x0        | Enable red led |

Back to [Register map](#register-map).

## RDFIFO

Read FIFO

Address offset: 0x04

Reset value: 0x0000

![](rmap_img/rdfifo.svg)

| Name             | Bits   | Mode            | Reset      | Description |
| :---             | :---   | :---            | :---       | :---        |
| FLUSH            | 15     | wo, sc          | 0x0        | Flush fifo data |
| -                | 14:12  | -               | 0x0        | Reserved |
| DATA             | 11:0   | ro, fifo        | 0x000      | Data to read. Data value will increment every time after read. |

Back to [Register map](#register-map).
