#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Corsair is a control and status register (CSR) map generator for FPGA/ASIC projects.
It generates HDL code, documentation and other artifacts from CSR map description file.
"""

from .__version__ import (
    __title__,
    __description__,
    __version__
)

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
    JSONReader,
    YAMLReader
)

from .writers import (
    JSONWriter,
    YAMLWriter
)

__all__ = [
    'Parameter',
    'ParameterGroup',
    'Configuration',
    'BitField',
    'Register',
    'RegisterMap',
    'JSONReader',
    'YAMLReader',
    'JSONWriter',
    'YAMLWriter'
]
