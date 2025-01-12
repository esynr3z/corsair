"""VHDL file generator for a register map."""

from __future__ import annotations

from typing import Literal

from .base import Generator, GeneratorConfig


class VhdlGenerator(Generator):
    """VHDL file generator for a register map."""

    class Config(GeneratorConfig):
        """Configuration for the VHDL generator."""

        kind: Literal["vhdl"]
        """Generator kind discriminator."""
