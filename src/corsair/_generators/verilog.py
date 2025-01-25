"""Verilog file generator for a register map."""

from __future__ import annotations

from typing import Literal

from .base import Generator, GeneratorConfig, ResetStyle


class VerilogGenerator(Generator):
    """Verilog file generator for a register map."""

    class Config(GeneratorConfig):
        """Configuration for the Verilog generator."""

        kind: Literal["verilog"] = "verilog"
        """Generator kind discriminator."""

        reset_style: ResetStyle = ResetStyle.ASYNC_NEG
        """Flip-flop reset style."""

        @property
        def generator_cls(self) -> type[Generator]:
            """Related generator class."""
            return VerilogGenerator
