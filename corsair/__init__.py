#!/usr/bin/env python3

"""Corsair is a control and status register (CSR) map generator for HDL projects.

It generates HDL code, documentation and other artifacts from CSR map description file.
"""

from __future__ import annotations

__title__ = "corsair"
__description__ = "Control and status register (CSR) map generator for HDL projects."


from .core import HwMode
from .input import (
    AnyTarget,
    BaseTarget,
    BuildSpecification,
    CustomTarget,
    ForceNameCase,
    GlobalConfig,
    MapCHeaderTarget,
    MapMarkdownTarget,
    MapSvPackageTarget,
    MapVerilogHeaderTarget,
    MapVerilogTarget,
    MapVhdlTarget,
    RegisterReset,
)
from .version import __version__

__all__ = (
    "__version__",
    # specification
    "BuildSpecification",
    # targets
    "AnyTarget",
    "BaseTarget",
    "CustomTarget",
    "MapVerilogTarget",
    "MapVhdlTarget",
    "MapSvPackageTarget",
    "MapVerilogHeaderTarget",
    "MapMarkdownTarget",
    "MapCHeaderTarget",
    # configuration
    "ForceNameCase",
    "RegisterReset",
    "GlobalConfig",
    # core
    "HwMode",
)
