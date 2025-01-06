#!/usr/bin/env python3

"""Corsair is a control and status register (CSR) map generator for HDL projects.

It generates HDL code, documentation and other artifacts from CSR map description file.
"""

from __future__ import annotations

__title__ = "corsair"
__description__ = "Control and status register (CSR) map generator for HDL projects."

from ._types import (
    IdentifierStr,
    Pow2Int,
    PyClassPathStr,
    SingleLineStr,
    TextStr,
)
from ._version import VERSION
from .input import (
    AnyTarget,
    BaseTarget,
    BuildSpecification,
    CustomTarget,
    GlobalConfig,
    MapCHeaderTarget,
    MapMarkdownTarget,
    MapSvPackageTarget,
    MapVerilogHeaderTarget,
    MapVerilogTarget,
    MapVhdlTarget,
    RegisterReset,
)

__version__ = VERSION

__all__ = (
    "VERSION",
    # types
    "IdentifierStr",
    "SingleLineStr",
    "TextStr",
    "PyClassPathStr",
    "Pow2Int",
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
    "RegisterReset",
    "GlobalConfig",
)
