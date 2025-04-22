"""Generators for output artifacts."""

from __future__ import annotations

from typing import Annotated

from pydantic import Field

from .base import (
    Generator,
    GeneratorConfig,
    GeneratorTemplateError,
    GeneratorUnsupportedFeatureError,
    ResetStyle,
)
from .markdown import MarkdownGenerator
from .verilog import VerilogGenerator
from .vhdl import VhdlGenerator
from .wavedrom import WaveDromGenerator

AnyGeneratorConfig = Annotated[
    VerilogGenerator.Config | VhdlGenerator.Config | MarkdownGenerator.Config | WaveDromGenerator.Config,
    Field(discriminator="kind"),
]

__all__ = [
    # Base classes
    "Generator",
    "GeneratorConfig",
    "ResetStyle",
    # Generators
    "VerilogGenerator",
    "VhdlGenerator",
    "MarkdownGenerator",
    "WaveDromGenerator",
    # Types
    "AnyGeneratorConfig",
    # Exceptions
    "GeneratorUnsupportedFeatureError",
    "GeneratorTemplateError",
]
