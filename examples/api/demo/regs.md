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
| [STAT](#stat)            | 0x0004     | Status register |
| [CTRL](#ctrl)            | 0x0008     | Control register |
| [LPMODE](#lpmode)        | 0x000c     | Low power mode control |
| [INTSTAT](#intstat)      | 0x0010     | Interrupt status register |
| [ID](#id)                | 0x0ffc     | IP-core ID register |

## DATA

Data register

Address offset: 0x0000

Reset value: 0x00000000


| Name             | Bits   | Mode            | Reset      | Description |
| :---             | :---   | :---            | :---       | :---        |
| -                | 31:18  | -               | 0x000      | Reserved |
| PERR             | 17     | rolh            | 0x0        | Parity error flag. Read to clear. |
| FERR             | 16     | rolh            | 0x0        | Frame error flag. Read to clear. |
| -                | 15:8   | -               | 0x00       | Reserved |
| FIFO             | 7:0    | rw              | 0x00       | Write to push value to TX FIFO, read to get data from RX FIFO |

Back to [Register map](#register-map-summary).

## STAT

Status register

Address offset: 0x0004

Reset value: 0x00000000


| Name             | Bits   | Mode            | Reset      | Description |
| :---             | :---   | :---            | :---       | :---        |
| -                | 31:6   | -               | 0x000000   | Reserved |
| TXF              | 5      | ro              | 0x0        | TX FIFO is full |
| RXE              | 4      | ro              | 0x0        | RX FIFO is empty |
| -                | 3:1    | -               | 0x0        | Reserved |
| BUSY             | 0      | ro              | 0x0        | Transciever is busy |

Back to [Register map](#register-map-summary).

## CTRL

Control register

Address offset: 0x0008

Reset value: 0x00000000


| Name             | Bits   | Mode            | Reset      | Description |
| :---             | :---   | :---            | :---       | :---        |
| -                | 31:7   | -               | 0x000000   | Reserved |
| TXST             | 6      | wosc            | 0x0        | Force transmission start |
| RXEN             | 5      | rw              | 0x0        | Receiver enable. Can be disabled by hardware on error. |
| TXEN             | 4      | rw              | 0x0        | Transmitter enable. Can be disabled by hardware on error. |
| -                | 3:2    | -               | 0x0        | Reserved |
| BAUD             | 1:0    | rw              | 0x0        | Baudrate value |

Enumerated values for CTRL.BAUD.

| Name             | Value   | Description |
| :---             | :---    | :---        |
| B9600            | 0x0    | 9600 baud |
| B38400           | 0x1    | 38400 baud |
| B115200          | 0x2    | 115200 baud |

Back to [Register map](#register-map-summary).

## LPMODE

Low power mode control

Address offset: 0x000c

Reset value: 0x00000000


| Name             | Bits   | Mode            | Reset      | Description |
| :---             | :---   | :---            | :---       | :---        |
| EN               | 31     | rw              | 0x0        | Low power mode enable |
| -                | 30:8   | -               | 0x00000    | Reserved |
| DIV              | 7:0    | rw              | 0x00       | Clock divider in low power mode |

Back to [Register map](#register-map-summary).

## INTSTAT

Interrupt status register

Address offset: 0x0010

Reset value: 0x00000000


| Name             | Bits   | Mode            | Reset      | Description |
| :---             | :---   | :---            | :---       | :---        |
| -                | 31:2   | -               | 0x0000000  | Reserved |
| RX               | 1      | rw1c            | 0x0        | Receiver interrupt. Write 1 to clear. |
| TX               | 0      | rw1c            | 0x0        | Transmitter interrupt flag. Write 1 to clear. |

Back to [Register map](#register-map-summary).

## ID

IP-core ID register

Address offset: 0x0ffc

Reset value: 0xcafe0666


| Name             | Bits   | Mode            | Reset      | Description |
| :---             | :---   | :---            | :---       | :---        |
| UID              | 31:0   | ro              | 0xcafe0666 | Unique ID |

Back to [Register map](#register-map-summary).
