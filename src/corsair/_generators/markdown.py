"""Markdown file generator for a register map."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Literal

from .base import Generator, GeneratorConfig
from .wavedrom import WaveDromGenerator

if TYPE_CHECKING:
    from collections.abc import Generator as TypeGenerator


class MarkdownGenerator(Generator):
    """Markdown file generator for a register map."""

    template_name: str = "regmap.md.j2"

    class Config(GeneratorConfig):
        """Configuration for the Markdown generator."""

        kind: Literal["markdown"] = "markdown"
        """Generator kind discriminator."""

        file_name: str = "regmap.md"
        """Name of the output file."""

        title: str = "Register Map"
        """Document title."""

        print_images: bool = False
        """Enable generating images for bit fields of a register."""

        image_dir: Path = Path("img")
        """Directory for storing images."""

        print_conventions: bool = True
        """Enable generating table with register access modes explained."""

        wavedrom: WaveDromGenerator.Config = WaveDromGenerator.Config()
        """Configuration for the WaveDrom generator."""

        @property
        def generator_cls(self) -> type[Generator]:
            """Related generator class."""
            return MarkdownGenerator

    @classmethod
    def get_config_cls(cls) -> type[GeneratorConfig]:
        """Get the configuration class for the generator."""
        return cls.Config

    def _generate(self) -> TypeGenerator[Path, None, None]:
        """Generate all the outputs."""
        if not isinstance(self.config, self.Config):
            raise TypeError("Configuration instance is not of the expected type of MarkdownGenerator.Config")

        context = {
            "cfg": self.config,
            "regmap": self.register_map,
        }

        yield self._render_to_file(
            template_name=self.template_name,
            context=context,
            file_name=self.config.file_name,
        )

        if self.config.print_images:
            wd_gen = WaveDromGenerator(
                label=f"{self.label}.wavedrom",
                register_map=self.register_map,
                config=self.config.wavedrom,
                output_dir=self.config.image_dir,
            )
            yield from wd_gen()
