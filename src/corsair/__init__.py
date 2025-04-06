#!/usr/bin/env python3

"""Corsair is a control and status register (CSR) map generator for HDL projects.

It generates HDL code, documentation and other artifacts from CSR map description file.
"""

from __future__ import annotations

__title__ = "corsair"
__description__ = "Control and status register (CSR) map generator for HDL projects."

from ._build import BuildSpecification
from ._generators import (
    AnyGeneratorConfig,
    CustomGeneratorConfig,
    Generator,
    GeneratorConfig,
    ResetStyle,
    VerilogGenerator,
    VhdlGenerator,
)
from ._loaders import (
    AnyLoaderConfig,
    CustomLoaderConfig,
    Loader,
    LoaderConfig,
    LoaderValidationError,
    PyModuleLoader,
    SerializedLoader,
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
    convert_schema_loc_to_path_loc,
    stringify_model_errors,
)
from ._templates import TemplateEnvironment, TemplateKind
from ._types import (
    IdentifierStr,
    Pow2Int,
    PyAttrPathStr,
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
    "PyAttrPathStr",
    "Pow2Int",
    # Build
    "BuildSpecification",
    # Loaders
    "Loader",
    "LoaderConfig",
    "CustomLoaderConfig",
    "AnyLoaderConfig",
    "LoaderValidationError",
    "SerializedLoader",
    "PyModuleLoader",
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
    "stringify_model_errors",
    "convert_schema_loc_to_path_loc",
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
