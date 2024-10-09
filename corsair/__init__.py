#!/usr/bin/env python3

"""Corsair is a control and status register (CSR) map generator for HDL projects.

It generates HDL code, documentation and other artifacts from CSR map description file.
"""

from __future__ import annotations

__title__ = "corsair"
__description__ = "Control and status register (CSR) map generator for HDL projects."

from . import config, generators
from .bitfield import BitField
from .enum import EnumValue
from .reg import Register
from .regmap import RegisterMap
from .version import __version__

__all__ = [
    "__version__",
    "RegisterMap",
    "Register",
    "EnumValue",
    "BitField",
    "config",
    "generators",
]
