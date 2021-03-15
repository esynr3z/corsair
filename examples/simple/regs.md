# regs

Created with [Corsair](https://github.com/esynr3z/corsair) vgit-latest.

Register map v1.42.

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
| [LEN](#len)              | 0x000      | Length of pulse | |
| [CNT](#cnt)              | 0x004      | Counter value | |
| [START](#start)          | 0x008      | Start processes | |
| [STAT](#stat)            | 0x010      | Status | |
| [CTL](#ctl)              | 0x020      | Control | |
| [FLAG](#flag)            | 0x024      | Flags | |
| [VERSION](#version)      | 0x040      | Current version | |

## LEN

Length of pulse

Address offset: 0x000

Reset value: 0x00000000

![](regs_img/len.svg)

| Name             | Bits   | Mode            | Reset      | Description |
| :---             | :---   | :---            | :---       | :---        |
| LEN              | 31:0   | rw              | 0x00000000 | Length of pulse |

Back to [Register map](#register-map).

## CNT

Counter value

Address offset: 0x004

Reset value: 0x00000000

![](regs_img/cnt.svg)

| Name             | Bits   | Mode            | Reset      | Description |
| :---             | :---   | :---            | :---       | :---        |
| -                | 31:16  | -               | 0x0000     | Reserved |
| CNT              | 15:0   | rw, hwu         | 0x0000     | Counter value |

Back to [Register map](#register-map).

## START

Start processes

Address offset: 0x008

Reset value: 0x00000000

![](regs_img/start.svg)

| Name             | Bits   | Mode            | Reset      | Description |
| :---             | :---   | :---            | :---       | :---        |
| KEY              | 31:24  | wo              | 0x00       | Secret key to start process |
| -                | 23:17  | -               | 0x0        | Reserved |
| STC              | 16     | wo, sc          | 0x0        | Start process C |
| -                | 15:9   | -               | 0x0        | Reserved |
| STB              | 8      | wo, sc          | 0x0        | Start process B |
| -                | 7:1    | -               | 0x0        | Reserved |
| STA              | 0      | wo, sc          | 0x0        | Start process A |

Back to [Register map](#register-map).

## STAT

Status

Address offset: 0x010

Reset value: 0x00000000

![](regs_img/stat.svg)

| Name             | Bits   | Mode            | Reset      | Description |
| :---             | :---   | :---            | :---       | :---        |
| -                | 31:6   | -               | 0x000000   | Reserved |
| STATE            | 5:3    | ro, hwu         | 0x0        | Current state |
| -                | 2:1    | -               | 0x0        | Reserved |
| DIR              | 0      | ro              | 0x0        | Current direction |

Back to [Register map](#register-map).

## CTL

Control

Address offset: 0x020

Reset value: 0x00000000

![](regs_img/ctl.svg)

| Name             | Bits   | Mode            | Reset      | Description |
| :---             | :---   | :---            | :---       | :---        |
| -                | 31:16  | -               | 0x0000     | Reserved |
| INITB            | 15:8   | rw              | 0x00       | Initial value for B |
| -                | 7:2    | -               | 0x0        | Reserved |
| ENA              | 1      | rw              | 0x0        | Enable A |

Back to [Register map](#register-map).

## FLAG

Flags

Address offset: 0x024

Reset value: 0x00000000

![](regs_img/flag.svg)

| Name             | Bits   | Mode            | Reset      | Description |
| :---             | :---   | :---            | :---       | :---        |
| -                | 31:3   | -               | 0x0000000  | Reserved |
| EVB              | 2      | ro, hwu, rtc    | 0x0        | Event B |
| -                | 1      | -               | 0x0        | Reserved |
| EVA              | 0      | rw, hwu, w1tc   | 0x0        | Event A |

Back to [Register map](#register-map).

## VERSION

Current version

Address offset: 0x040

Reset value: 0x00020023

![](regs_img/version.svg)

| Name             | Bits   | Mode            | Reset      | Description |
| :---             | :---   | :---            | :---       | :---        |
| -                | 31:24  | -               | 0x00       | Reserved |
| MAJOR            | 23:16  | ro, const       | 0x02       | Major version |
| -                | 15:8   | -               | 0x00       | Reserved |
| MINOR            | 7:0    | ro, const       | 0x23       | Minor version |

Back to [Register map](#register-map).
