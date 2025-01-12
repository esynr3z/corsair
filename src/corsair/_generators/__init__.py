"""Generators for output artifacts."""

from __future__ import annotations

from typing import Annotated

from pydantic import Field

from .base import CustomGeneratorConfig, Generator, GeneratorConfig, ResetStyle
from .verilog import VerilogGenerator
from .vhdl import VhdlGenerator

AnyGeneratorConfig = Annotated[
    CustomGeneratorConfig | VerilogGenerator.Config | VhdlGenerator.Config,
    Field(discriminator="kind"),
]

__all__ = [
    # Base classes
    "Generator",
    "GeneratorConfig",
    "CustomGeneratorConfig",
    "ResetStyle",
    # Generators
    "VerilogGenerator",
    "VhdlGenerator",
    # Types
    "AnyGeneratorConfig",
]
