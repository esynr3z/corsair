"""VHDL file generator for a register map."""

from __future__ import annotations

from typing import Literal

from .base import Generator, GeneratorConfig, ResetStyle


class VhdlGenerator(Generator):
    """VHDL file generator for a register map."""

    class Config(GeneratorConfig):
        """Configuration for the VHDL generator."""

        kind: Literal["vhdl"] = "vhdl"
        """Generator kind discriminator."""

        reset_style: ResetStyle = ResetStyle.ASYNC_NEG
        """Flip-flop reset style."""

        @property
        def generator_cls(self) -> type[Generator]:
            """Related generator class."""
            return VhdlGenerator
