# Corsair

![corsair_arch](https://raw.githubusercontent.com/esynr3z/corsair/master/docs/arch.svg)

Corsair is a tool that makes it easy to organize and support control and status register (CSR) map for any FPGA/ASIC project.
You just need to create and fill single CSR map description file once and then generate HDL code, headers, documentation and etc.

It is as easy as:

* Create CSR map description file or generate a template with Corsair:

```sh
corsair -t ip_csr.json
```

* Make changes to ```ip_csr.json```
* Generate output artifacts:

```sh
corsair -i ip_csr.json -o ip_regmap.v ip_regmap.md
```

Supported input formats:

* JSON
* YAML

Supported output formats:

* JSON
* YAML
* (**SOON**) Verilog
* (**SOON**) Markdown

For more details about ways the tool can be used and how it works please refer the documentation at [Read the docs](https://corsair.readthedocs.io).

## Installation

You can install the latest stable version from pypi:

```sh
python3 -m pip install -U corsair
```

## Development

Corsair is still under development. Please follow the [Developers Guide](https://corsair.readthedocs.io/en/latest/contributing.html).

## License

Corsair is licensed under [MIT License](LICENSE.txt).
