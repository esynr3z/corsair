#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Corsair is a control and status register (CSR) map generator for FPGA/ASIC projects.
It generates HDL code, documentation and other artifacts from CSR map description file.
"""

__title__ = "corsair"
__description__ = "Control and status register (CSR) map generator for FPGA/ASIC projects."

try:
    from ._version import version as __version__
except (ImportError, ModuleNotFoundError) as e:
    __version__ = 'git-latest'

from .config import (
    Parameter,
    ParameterGroup,
    Configuration
)

from .regmap import (
    BitField,
    Register,
    RegisterMap
)

from .readers import (
    RegisterMapReader,
    ConfigurationReader
)

from .writers import (
    RegisterMapWriter,
    ConfigurationWriter,
    LbBridgeWriter,
    HdlWriter,
    DocsWriter,
)
