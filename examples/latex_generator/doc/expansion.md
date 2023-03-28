# Expansion Register Map

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
| [GPIO0_VALUE](#gpio0_value) | 0x80       | GPIO0 Value |
| [GPIO0_DIR](#gpio0_dir)  | 0x81       | GPIO0 Direction |
| [GPIO1_VALUE](#gpio1_value) | 0x82       | GPIO1 Value |
| [GPIO1_DIR](#gpio1_dir)  | 0x83       | GPIO1 Direction |
| [GPIO2_VALUE](#gpio2_value) | 0x84       | GPIO2 Value |
| [GPIO2_DIR](#gpio2_dir)  | 0x85       | GPIO2 Direction |
| [GPIO3_VALUE](#gpio3_value) | 0x86       | GPIO3 Value |
| [GPIO3_DIR](#gpio3_dir)  | 0x87       | GPIO3 Direction |
| [CONTROL](#control)      | 0x88       | Control Register |
| [SM_FAULT](#sm_fault)    | 0x89       | SM Fault Register |
| [GPIO_CNT_CTL](#gpio_cnt_ctl) | 0x8f       | Deserializer GPIO Edge Counter Control |
| [DES0_GPIO_RE_CNT](#des0_gpio_re_cnt) | 0x90       | Deserializer #0 GPIO Rising Edge Counter |
| [DES0_GPIO_FE_CNT](#des0_gpio_fe_cnt) | 0x91       | Deserializer #0 GPIO Falling Edge Counter |
| [DES1_GPIO_RE_CNT](#des1_gpio_re_cnt) | 0x92       | Deserializer #1 GPIO Rising Edge Counter |
| [DES1_GPIO_FE_CNT](#des1_gpio_fe_cnt) | 0x93       | Deserializer #1 GPIO Falling Edge Counter |
| [GPIO4_VALUE](#gpio4_value) | 0x9e       | GPIO4 Value |
| [GPIO4_DIR](#gpio4_dir)  | 0x9f       | GPIO4 Direction |

## GPIO0_VALUE

GPIO0 Value

Address offset: 0x80

Reset value: 0x00

![gpio0_value](md_img/gpio0_value.svg)

| Name             | Bits   | Mode            | Reset      | Description |
| :---             | :---   | :---            | :---       | :---        |
| RES              | 7:6    | ro              | 0x0        | Reserved |
| GPIO0\_5         | 5      | rw              | 0x0        | Deserializer #0 GENERAL_IO5 Value |
| GPIO0\_4         | 4      | rw              | 0x0        | Deserializer #0 GENERAL_IO4 Value |
| GPIO0\_3         | 3      | rw              | 0x0        | Deserializer #0 GENERAL_IO3 Value |
| GPIO0\_2         | 2      | rw              | 0x0        | Deserializer #0 GENERAL_IO2 Value |
| RES              | 1:0    | ro              | 0x0        | Reserved |

Back to [Register map](#register-map-summary).

## GPIO0_DIR

GPIO0 Direction

Address offset: 0x81

Reset value: 0x00

![gpio0_dir](md_img/gpio0_dir.svg)

| Name             | Bits   | Mode            | Reset      | Description |
| :---             | :---   | :---            | :---       | :---        |
| RES              | 7:6    | ro              | 0x0        | Reserved |
| GPIO0\_5\_DIR    | 5      | rw              | 0x0        | FPGA Pin to Deserializer #0 GENERAL_IO4 is Input (0) / Output (1) |
| GPIO0\_4\_DIR    | 4      | rw              | 0x0        | FPGA Pin to Deserializer #0 GENERAL_IO4 is Input (0) / Output (1) |
| GPIO0\_3\_DIR    | 3      | rw              | 0x0        | FPGA Pin to Deserializer #0 GENERAL_IO3 is Input (0) / Output (1) |
| GPIO0\_2\_DIR    | 2      | rw              | 0x0        | FPGA Pin to Deserializer #0 GENERAL_IO2 is Input (0) / Output (1) |
| RES              | 1:0    | ro              | 0x0        | Reserved |

Back to [Register map](#register-map-summary).

## GPIO1_VALUE

GPIO1 Value

Address offset: 0x82

Reset value: 0x00

![gpio1_value](md_img/gpio1_value.svg)

| Name             | Bits   | Mode            | Reset      | Description |
| :---             | :---   | :---            | :---       | :---        |
| RES              | 7:6    | ro              | 0x0        | Reserved |
| GPIO1\_5         | 5      | rw              | 0x0        | Deserializer #1 GENERAL_IO5 Value |
| GPIO1\_4         | 4      | rw              | 0x0        | Deserializer #1 GENERAL_IO4 Value |
| GPIO1\_3         | 3      | rw              | 0x0        | Deserializer #1 GENERAL_IO3 Value |
| GPIO1\_2         | 2      | rw              | 0x0        | Deserializer #1 GENERAL_IO2 Value |
| RES              | 1:0    | ro              | 0x0        | Reserved |

Back to [Register map](#register-map-summary).

## GPIO1_DIR

GPIO1 Direction

Address offset: 0x83

Reset value: 0x00

![gpio1_dir](md_img/gpio1_dir.svg)

| Name             | Bits   | Mode            | Reset      | Description |
| :---             | :---   | :---            | :---       | :---        |
| RES              | 7:6    | ro              | 0x0        | Reserved |
| GPIO1\_5\_DIR    | 5      | rw              | 0x0        | FPGA Pin to Deserializer #1 GENERAL_IO4 is Input (0) / Output (1) |
| GPIO1\_4\_DIR    | 4      | rw              | 0x0        | FPGA Pin to Deserializer #1 GENERAL_IO4 is Input (0) / Output (1) |
| GPIO1\_3\_DIR    | 3      | rw              | 0x0        | FPGA Pin to Deserializer #1 GENERAL_IO3 is Input (0) / Output (1) |
| GPIO1\_2\_DIR    | 2      | rw              | 0x0        | FPGA Pin to Deserializer #1 GENERAL_IO2 is Input (0) / Output (1) |
| RES              | 1:0    | ro              | 0x0        | Reserved |

Back to [Register map](#register-map-summary).

## GPIO2_VALUE

GPIO2 Value

Address offset: 0x84

Reset value: 0x00

![gpio2_value](md_img/gpio2_value.svg)

| Name             | Bits   | Mode            | Reset      | Description |
| :---             | :---   | :---            | :---       | :---        |
| RES              | 7:5    | ro              | 0x0        | Reserved |
| GPIO2\_4         | 4      | rw              | 0x0        | Serializer #0 GENERAL_IO4 Value |
| GPIO2\_3         | 3      | rw              | 0x0        | Serializer #0 GENERAL_IO3 Value |
| GPIO2\_2         | 2      | rw              | 0x0        | Serializer #0 GENERAL_IO2 Value |
| RES              | 1:0    | ro              | 0x0        | Reserved |

Back to [Register map](#register-map-summary).

## GPIO2_DIR

GPIO2 Direction

Address offset: 0x85

Reset value: 0x00

![gpio2_dir](md_img/gpio2_dir.svg)

| Name             | Bits   | Mode            | Reset      | Description |
| :---             | :---   | :---            | :---       | :---        |
| RES              | 7:5    | ro              | 0x0        | Reserved |
| GPIO2\_4\_DIR    | 4      | rw              | 0x0        | FPGA Pin to Serializer #0 GENERAL_IO4 is Input (0) / Output (1) |
| GPIO2\_3\_DIR    | 3      | rw              | 0x0        | FPGA Pin to Serializer #0 GENERAL_IO3 is Input (0) / Output (1) |
| GPIO2\_2\_DIR    | 2      | rw              | 0x0        | FPGA Pin to Serializer #0 GENERAL_IO2 is Input (0) / Output (1) |
| RES              | 1:0    | ro              | 0x0        | Reserved |

Back to [Register map](#register-map-summary).

## GPIO3_VALUE

GPIO3 Value

Address offset: 0x86

Reset value: 0x00

![gpio3_value](md_img/gpio3_value.svg)

| Name             | Bits   | Mode            | Reset      | Description |
| :---             | :---   | :---            | :---       | :---        |
| RES              | 7:5    | ro              | 0x0        | Reserved |
| GPIO3\_4         | 4      | rw              | 0x0        | Serializer #1 GENERAL_IO4 Value |
| GPIO3\_3         | 3      | rw              | 0x0        | Serializer #1 GENERAL_IO3 Value |
| GPIO3\_2         | 2      | rw              | 0x0        | Serializer #1 GENERAL_IO2 Value |
| RES              | 1:0    | ro              | 0x0        | Reserved |

Back to [Register map](#register-map-summary).

## GPIO3_DIR

GPIO3 Direction

Address offset: 0x87

Reset value: 0x00

![gpio3_dir](md_img/gpio3_dir.svg)

| Name             | Bits   | Mode            | Reset      | Description |
| :---             | :---   | :---            | :---       | :---        |
| RES              | 7:5    | ro              | 0x0        | Reserved |
| GPIO3\_4\_DIR    | 4      | rw              | 0x0        | FPGA Pin to Serializer #1 GENERAL_IO4 is Input (0) / Output (1) |
| GPIO3\_3\_DIR    | 3      | rw              | 0x0        | FPGA Pin to Serializer #1 GENERAL_IO3 is Input (0) / Output (1) |
| GPIO3\_2\_DIR    | 2      | rw              | 0x0        | FPGA Pin to Serializer #1 GENERAL_IO2 is Input (0) / Output (1) |
| RES              | 1:0    | ro              | 0x0        | Reserved |

Back to [Register map](#register-map-summary).

## CONTROL

Control Register

Address offset: 0x88

Reset value: 0x00

![control](md_img/control.svg)

| Name             | Bits   | Mode            | Reset      | Description |
| :---             | :---   | :---            | :---       | :---        |
| POC2\_BYP\_ERR   | 7      | ro              | 0x0        | PoC 2 Bypass Error |
| POC2\_BYP\_EN    | 6      | rw              | 0x0        | PoC 2 Bypass Enable |
| POC2\_ERR        | 5      | ro              | 0x0        | PoC 2 Error |
| POC2\_EN         | 4      | rw              | 0x0        | PoC 2 Enable |
| POC1\_BYP\_ERR   | 3      | ro              | 0x0        | PoC 1 Bypass Error |
| POC1\_BYP\_EN    | 2      | rw              | 0x0        | PoC 1 Bypass Enable |
| POC1\_ERR        | 1      | ro              | 0x0        | PoC 1 Error |
| POC1\_EN         | 0      | rw              | 0x0        | PoC 1 Enable |

Back to [Register map](#register-map-summary).

## SM_FAULT

SM Fault Register

Address offset: 0x89

Reset value: 0x00

![sm_fault](md_img/sm_fault.svg)

| Name             | Bits   | Mode            | Reset      | Description |
| :---             | :---   | :---            | :---       | :---        |
| RES              | 7      | ro              | 0x0        | Reserved |
| SER1\_EXT\_SM\_FAULT | 6      | ro              | 0x0        | Serializer 1 EXT SM Fault |
| RES              | 5      | ro              | 0x0        | Reserved |
| SER0\_EXT\_SM\_FAULT | 4      | ro              | 0x0        | Serializer 0 EXT SM Fault |
| DES1\_SM\_FAULT  | 3      | ro              | 0x0        | Deserializer 1 SM Fault |
| DES1\_EXT\_SM\_FAULT | 2      | ro              | 0x0        | Deserializer 1 EXT SM Fault |
| DES0\_SM\_FAULT  | 1      | ro              | 0x0        | Deserializer 0 SM Fault |
| DES0\_EXT\_SM\_FAULT | 0      | ro              | 0x0        | Deserializer 0 EXT SM Fault |

Back to [Register map](#register-map-summary).

## GPIO_CNT_CTL

Deserializer GPIO Edge Counter Control

Address offset: 0x8f

Reset value: 0x00

![gpio_cnt_ctl](md_img/gpio_cnt_ctl.svg)

| Name             | Bits   | Mode            | Reset      | Description |
| :---             | :---   | :---            | :---       | :---        |
| DES1\_GPIO\_SEL  | 7:4    | rw              | 0x0        | Deserializer #1 GPIO Select |
| DES0\_GPIO\_SEL  | 3:0    | rw              | 0x0        | Deserializer #0 GPIO Select |

Enumerated values for GPIO_CNT_CTL.DES0_GPIO_SEL.

| Name             | Value   | Description |
| :---             | :---    | :---        |
| GENERAL\_IO0     | 0x0    | Deserializer #0 GENERAL_IO0 |
| GENERAL\_IO1     | 0x1    | Deserializer #0 GENERAL_IO1 |
| GENERAL\_IO2     | 0x2    | Deserializer #0 GENERAL_IO2 |
| GENERAL\_IO3     | 0x3    | Deserializer #0 GENERAL_IO3 |
| GENERAL\_IO4     | 0x4    | Deserializer #0 GENERAL_IO4 |
| GENERAL\_IO5     | 0x5    | Deserializer #0 GENERAL_IO5 |

Enumerated values for GPIO_CNT_CTL.DES1_GPIO_SEL.

| Name             | Value   | Description |
| :---             | :---    | :---        |
| GENERAL\_IO0     | 0x0    | Deserializer #1 GENERAL_IO0 |
| GENERAL\_IO1     | 0x1    | Deserializer #1 GENERAL_IO1 |
| GENERAL\_IO2     | 0x2    | Deserializer #1 GENERAL_IO2 |
| GENERAL\_IO3     | 0x3    | Deserializer #1 GENERAL_IO3 |
| GENERAL\_IO4     | 0x4    | Deserializer #1 GENERAL_IO4 |
| GENERAL\_IO5     | 0x5    | Deserializer #1 GENERAL_IO5 |

Back to [Register map](#register-map-summary).

## DES0_GPIO_RE_CNT

Deserializer #0 GPIO Rising Edge Counter

Address offset: 0x90

Reset value: 0x00

![des0_gpio_re_cnt](md_img/des0_gpio_re_cnt.svg)

| Name             | Bits   | Mode            | Reset      | Description |
| :---             | :---   | :---            | :---       | :---        |
| EDGE\_CNT        | 7:0    | roc             | 0x00       | Deserializer #0 Rising Edge Counter. Count the rising edges of the selected Deserializer #0 GENERAL_IO. |

Back to [Register map](#register-map-summary).

## DES0_GPIO_FE_CNT

Deserializer #0 GPIO Falling Edge Counter

Address offset: 0x91

Reset value: 0x00

![des0_gpio_fe_cnt](md_img/des0_gpio_fe_cnt.svg)

| Name             | Bits   | Mode            | Reset      | Description |
| :---             | :---   | :---            | :---       | :---        |
| EDGE\_CNT        | 7:0    | roc             | 0x00       | Deserializer #0 Falling Edge Counter. Count the rising edges of the selected Deserializer #0 GENERAL_IO. |

Back to [Register map](#register-map-summary).

## DES1_GPIO_RE_CNT

Deserializer #1 GPIO Rising Edge Counter

Address offset: 0x92

Reset value: 0x00

![des1_gpio_re_cnt](md_img/des1_gpio_re_cnt.svg)

| Name             | Bits   | Mode            | Reset      | Description |
| :---             | :---   | :---            | :---       | :---        |
| EDGE\_CNT        | 7:0    | roc             | 0x00       | Deserializer #1 Rising Edge Counter. Count the rising edges of the selected Deserializer #1 GENERAL_IO. |

Back to [Register map](#register-map-summary).

## DES1_GPIO_FE_CNT

Deserializer #1 GPIO Falling Edge Counter

Address offset: 0x93

Reset value: 0x00

![des1_gpio_fe_cnt](md_img/des1_gpio_fe_cnt.svg)

| Name             | Bits   | Mode            | Reset      | Description |
| :---             | :---   | :---            | :---       | :---        |
| EDGE\_CNT        | 7:0    | roc             | 0x00       | Deserializer #1 Falling Edge Counter. Count the falling edges of the selected Deserializer #1 GENERAL_IO. |

Back to [Register map](#register-map-summary).

## GPIO4_VALUE

GPIO4 Value

Address offset: 0x9e

Reset value: 0x00

![gpio4_value](md_img/gpio4_value.svg)

| Name             | Bits   | Mode            | Reset      | Description |
| :---             | :---   | :---            | :---       | :---        |
| RES              | 7:4    | ro              | 0x0        | Reserved |
| GPIO4\_3         | 3      | rw              | 0x0        | Net 'SPI_MISO Value' |
| GPIO4\_2         | 2      | rw              | 0x0        | Net 'SPI_MOSI Value' |
| GPIO4\_1         | 1      | rw              | 0x0        | Net 'SPI_CS Value' |
| GPIO4\_0         | 0      | rw              | 0x0        | Net 'SPI_CLK Value' |

Back to [Register map](#register-map-summary).

## GPIO4_DIR

GPIO4 Direction

Address offset: 0x9f

Reset value: 0x00

![gpio4_dir](md_img/gpio4_dir.svg)

| Name             | Bits   | Mode            | Reset      | Description |
| :---             | :---   | :---            | :---       | :---        |
| RES              | 7:4    | ro              | 0x0        | Reserved |
| GPIO4\_5\_DIR    | 3      | rw              | 0x0        | FPGA Pin to net 'SPI_MISO' is Input (0) / Output (1) |
| GPIO4\_4\_DIR    | 2      | rw              | 0x0        | FPGA Pin to net 'SPI_MOSI' is Input (0) / Output (1) |
| GPIO4\_3\_DIR    | 1      | rw              | 0x0        | FPGA Pin to net 'SPI_CS' is Input (0) / Output (1) |
| GPIO4\_2\_DIR    | 0      | rw              | 0x0        | FPGA Pin to net 'SPI_CLK' is Input (0) / Output (1) |

Back to [Register map](#register-map-summary).
