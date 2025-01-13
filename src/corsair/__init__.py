#!/usr/bin/env python3

"""Corsair is a control and status register (CSR) map generator for HDL projects.

It generates HDL code, documentation and other artifacts from CSR map description file.
"""

from __future__ import annotations

__title__ = "corsair"
__description__ = "Control and status register (CSR) map generator for HDL projects."

from ._generators import (
    AnyGeneratorConfig,
    CustomGeneratorConfig,
    Generator,
    GeneratorConfig,
    ResetStyle,
    VerilogGenerator,
    VhdlGenerator,
)
from ._model import (
    AccessCategory,
    AccessMode,
    ArrayItem,
    Enum,
    EnumMember,
    Field,
    FieldArray,
    HardwareMode,
    ItemMetadata,
    Map,
    MapableItem,
    MapArray,
    Memory,
    MemoryArray,
    MemoryStyle,
    NamedItem,
    Register,
    RegisterArray,
)
from ._parsers import (
    AnyParserConfig,
    CustomParserConfig,
    Deserializer,
    Parser,
    ParserConfig,
)
from ._templates import TemplateEnvironment, TemplateKind
from ._types import (
    IdentifierStr,
    Pow2Int,
    PyClassPathStr,
    SingleLineStr,
    TextStr,
)
from ._version import VERSION

__version__ = VERSION

__all__ = (
    # Globals
    "VERSION",
    # Common types
    "IdentifierStr",
    "SingleLineStr",
    "TextStr",
    "PyClassPathStr",
    "Pow2Int",
    # Parsers
    "Parser",
    "ParserConfig",
    "CustomParserConfig",
    "AnyParserConfig",
    "Deserializer",
    # CSR model
    "AccessMode",
    "AccessCategory",
    "MemoryStyle",
    "HardwareMode",
    "ItemMetadata",
    "NamedItem",
    "MapableItem",
    "ArrayItem",
    "EnumMember",
    "Enum",
    "Field",
    "Register",
    "Memory",
    "Map",
    "FieldArray",
    "RegisterArray",
    "MemoryArray",
    "MapArray",
    # Generators
    "ResetStyle",
    "Generator",
    "GeneratorConfig",
    "CustomGeneratorConfig",
    "AnyGeneratorConfig",
    "VerilogGenerator",
    "VhdlGenerator",
    # Templates
    "TemplateEnvironment",
    "TemplateKind",
)
