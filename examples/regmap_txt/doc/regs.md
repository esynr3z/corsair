# Register map

Created with [Corsair](https://github.com/esynr3z/corsair) vgit-latest.

## Conventions

| Access mode | Description               |
| :---------- | :------------------------ |
| rw          | Read and Write            |
| rw1c        | Read and Write 1 to Clear |
| rw1s        | Read and Write 1 to Set   |
| ro          | Read Only                 |
| roc         | Read Only to Clear        |
| roll        | Read Only / Latch Low     |
| rolh        | Read Only / Latch High    |
| wo          | Write only                |
| wosc        | Write Only / Self Clear   |

## Register map summary

Base address: 0x00000000

| Name                     | Address    | Description |
| :---                     | :---       | :---        |
| [DATA](#data)            | 0x0000     | Data register |
| [CTRL](#ctrl)            | 0x0004     | Control register |
| [STATUS](#status)        | 0x0008     | Status register |
| [START](#start)          | 0x0100     | Start register |

## DATA

Data register

Address offset: 0x0000

Reset value: 0x00000000

![data](regs_img/data.svg)

| Name             | Bits   | Mode            | Reset      | Description |
| :---             | :---   | :---            | :---       | :---        |
| val              | 31:0   | rw              | 0x00000000 | Value of the register |

Back to [Register map](#register-map-summary).

## CTRL

Control register

Address offset: 0x0004

Reset value: 0x00000100

![ctrl](regs_img/ctrl.svg)

| Name             | Bits   | Mode            | Reset      | Description |
| :---             | :---   | :---            | :---       | :---        |
| -                | 31:16  | -               | 0x0000     | Reserved |
| val              | 15:0   | rw              | 0x0100     | Value of the register |

Back to [Register map](#register-map-summary).

## STATUS

Status register

Address offset: 0x0008

Reset value: 0x00000000

![status](regs_img/status.svg)

| Name             | Bits   | Mode            | Reset      | Description |
| :---             | :---   | :---            | :---       | :---        |
| -                | 31:8   | -               | 0x000000   | Reserved |
| val              | 7:0    | ro              | 0x00       | Value of the register |

Back to [Register map](#register-map-summary).

## START

Start register

Address offset: 0x0100

Reset value: 0x00000000

![start](regs_img/start.svg)

| Name             | Bits   | Mode            | Reset      | Description |
| :---             | :---   | :---            | :---       | :---        |
| -                | 31:1   | -               | 0x0000000  | Reserved |
| val              | 0      | wosc            | 0x0        | Value of the register |

Back to [Register map](#register-map-summary).
