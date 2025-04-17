"""Generator for WaveDrom bit field images from a register map."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING, Literal

from pydantic import Field as PydanticField

from .base import Generator, GeneratorConfig

if TYPE_CHECKING:
    from collections.abc import Generator as TypeGenerator
    from pathlib import Path


class WaveDromGenerator(Generator):
    """WaveDrom bit field images generator for a register map."""

    class Config(GeneratorConfig):
        """Configuration for the WaveDrom generator."""

        kind: Literal["wavedrom"] = "wavedrom"
        """Generator kind discriminator."""

        vspace: int = PydanticField(default=80, ge=20)
        """Vertical space between lanes."""

        hspace: int = PydanticField(default=800, ge=40)
        """Horizontal space between lanes."""

        lanes: int = PydanticField(default=1, ge=1)
        """Number of lanes."""

        bits: int = PydanticField(default=32, ge=4)
        """Overall bit width."""

        hflip: bool = False
        """Horizontal flip."""

        vflip: bool = False
        """Vertical flip."""

        fontsize: int = PydanticField(default=14, ge=6)
        """Font size."""

        fontfamily: str = "sans-serif"
        """Font family."""

        fontweight: str = "normal"
        """Font weight."""

        use_bits_from_map: bool = True
        """Use the bit width from the register map. When True, `bits` is ignored."""

        dump_json: bool = False
        """Dump the JSON wavedrom descriptions for every register."""

        render_svg: bool = True
        """Render the SVG images."""

        @property
        def generator_cls(self) -> type[Generator]:
            """Related generator class."""
            return WaveDromGenerator

    @classmethod
    def get_config_cls(cls) -> type[GeneratorConfig]:
        """Get the configuration class for the generator."""
        return cls.Config

    def _pre_generate(self) -> None:
        """Pre-generate hook."""

    def _generate(self) -> TypeGenerator[Path, None, None]:
        """Generate all the outputs."""
        if not isinstance(self.config, self.Config):
            raise TypeError("Configuration instance is not of the expected type of WaveDromGenerator.Config")

        # Prepare the config for the WaveDrom library
        config_dict = {
            "vspace": self.config.vspace,
            "hspace": self.config.hspace,
            "lanes": self.config.lanes,
            "bits": self.register_map.register_width if self.config.use_bits_from_map else self.config.bits,
            "hflip": self.config.hflip,
            "vflip": self.config.vflip,
            "fontsize": self.config.fontsize,
            "fontfamily": self.config.fontfamily,
            "fontweight": self.config.fontweight,
        }

        for reg in self.register_map.registers:
            file_name = f"{self.register_map.name}_{reg.name}"

            # Prepare the fields
            fields = []
            for field in reg.fields_with_reserved:
                if field.name.startswith("_reserved"):
                    fields.append({"bits": field.width})
                else:
                    fields.append(
                        {
                            "name": field.name.upper(),
                            "bits": field.width,
                            "attr": field.access.value.upper(),
                        }
                    )

            # Save the JSON description
            if self.config.dump_json:
                json_file = self.output_dir / f"{file_name}.json"
                with json_file.open("w") as f:
                    json.dump({"reg": fields, "config": config_dict}, f)
                yield json_file

            # Render and save the SVG image
            try:
                from wavedrom.bitfield import BitField as WaveDromField
                from wavedrom.bitfield import Options as WaveDromFieldOptions

                svg_file = self.output_dir / f"{file_name}.svg"
                WaveDromField().render(fields, WaveDromFieldOptions(**config_dict)).saveas(svg_file)
                yield svg_file
            except ImportError as e:
                raise ImportError(
                    "wavedrom is not installed. "
                    "Try installing it with `pip install corsair[wavedrom]` or `pip install corsair[full]`."
                ) from e
