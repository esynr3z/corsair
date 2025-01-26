"""Verilog file generator for a register map."""

from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from .base import Generator, GeneratorConfig, ResetStyle

if TYPE_CHECKING:
    from collections.abc import Iterator
    from pathlib import Path


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

    @classmethod
    def get_config_cls(cls) -> type[GeneratorConfig]:
        """Get the configuration class for the generator."""
        return cls.Config

    def __call__(self, output_dir: Path, dry_run: bool = False) -> Iterator[Path]:
        """Generate all the outputs."""
        raise NotImplementedError
