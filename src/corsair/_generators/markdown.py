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

    class Config(GeneratorConfig):
        """Configuration for the Markdown generator."""

        kind: Literal["markdown"] = "markdown"
        """Generator kind discriminator."""

        file_name: str = "regmap.md"
        """Name of the output file."""

        title: str = "Register Map"
        """Document title."""

        template_name: str = "regmap.md.j2"
        """Name of the Jinja2 template to use."""

        print_images: bool = False
        """Enable generating images for bit fields of a register."""

        image_dir: Path = Path("img")
        """Directory for storing images."""

        print_conventions: bool = True
        """Enable generating table with register access modes explained."""

        print_disclaimer: bool = True
        """Enable generating disclaimer with version at the beginning of the file."""

        wavedrom: WaveDromGenerator.Config = WaveDromGenerator.Config()
        """Configuration for the WaveDrom generator."""

        @property
        def generator_cls(self) -> type[Generator]:
            """Related generator class."""
            return MarkdownGenerator

        def get_kind(self) -> str:
            """Get the kind of the generator."""
            return self.kind

    @classmethod
    def get_config_cls(cls) -> type[GeneratorConfig]:
        """Get the configuration class for the generator."""
        return cls.Config

    def _generate(self) -> TypeGenerator[Path, None, None]:
        """Generate all the outputs."""
        assert isinstance(self.config, self.Config)  # noqa: S101, to help type checker

        context = {
            "cfg": self.config,
            "regmap": self.register_map,
        }

        yield self._render_to_file(
            template_name=self.config.template_name,
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
