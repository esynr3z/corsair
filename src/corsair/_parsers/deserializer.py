"""Parser for serialized register maps (JSON, JSON5, YAML, etc.)."""

from __future__ import annotations

from typing import Literal

from .base import Parser, ParserConfig


class Deserializer(Parser):
    """Parse register map from serialized format (JSON, JSON5, YAML, etc.)."""

    class Config(ParserConfig):
        """Configuration for the serialized parser."""

        kind: Literal["json", "yaml"]
        """Parser kind discriminator."""
