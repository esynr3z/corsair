#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Corsair is a control and status register (CSR) map generator for HDL projects.
It generates HDL code, documentation and other artifacts from CSR map description file.
"""

__title__ = "corsair"
__description__ = "Control and status register (CSR) map generator for HDL projects."

try:
    from ._version import version as __version__
except (ImportError, ModuleNotFoundError) as e:
    __version__ = 'git-latest'

from . import config
from .enum import EnumValue
from .bitfield import BitField
from .reg import Register
from .regmap import RegisterMap
from . import generators
