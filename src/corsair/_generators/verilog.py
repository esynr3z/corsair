"""Verilog file generator for a register map."""

from __future__ import annotations

from typing import Literal

from .base import Generator, GeneratorConfig


class VerilogGenerator(Generator):
    """Verilog file generator for a register map."""

    class Config(GeneratorConfig):
        """Configuration for the Verilog generator."""

        kind: Literal["verilog"]
        """Generator kind discriminator."""
