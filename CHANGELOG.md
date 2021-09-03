## 1.0.0 (2021-09-03)

**Reworking the entire project almost from scratch. Lots of breaking changes.**

* New configuration file format (INI)
* New file generation flow (more clear)
* Do refactoring of all core modules
* Add enums
* Add C header generator
* Add Verilog header generator
* Add SystemVerilog package generator
* Embed bus interface (AXI-Lite, APB, Avalon-MM) into a register map
* Add VHDL register map generator
* Add plenty of examples
* Rework of documentation
* Update the tests
* Many minor tweaks and fixes


## 0.3.0 (2021-02-21)

* Fix Markdown table row endings.
* Add 'Reserved' bitfields to Markdown.
* Fix installation guides.
* Implement access_strobes attribute for register.
* Implement complementary registers.
* Implement write_lock attribute for register.
* Implement FIFO bitfield modifier.
* Implement AXI-Lite to Local Bus bridge on Verilog.
* Implement Avalon-MM to Local Bus bridge on Verilog.

## 0.2.0 (2021-01-08)

* Rework CLI keys
* Fix entry point for CLI
* Add Verilog and Markdown writers for a register map
* Add Local Bus bridge writer
* Implement APB to Local Bus bridge on Verilog
* Setup HDL testing environment
* Setup CI/CD via Github Actions
* Documentation fixes, code prettifying and etc.

## 0.1.0 (2020-12-16)

* Setup repository
* Setup documentation
* Setup testing
* Implementation of core classes
* Add support of running from a command line
* Add JSON and YAML readers
* Add JSON and YAML writers
