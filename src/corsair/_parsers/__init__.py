"""Parsers for register maps."""

from __future__ import annotations

from typing import Annotated

from pydantic import Field

from .base import CustomParserConfig, Parser, ParserConfig
from .deserializer import Deserializer

AnyParserConfig = Annotated[
    CustomParserConfig,
    Deserializer.Config,
    Field(discriminator="kind"),
]

__all__ = [
    # Base classes
    "Parser",
    "ParserConfig",
    "CustomParserConfig",
    # Parsers
    "Deserializer",
    # Types
    "AnyParserConfig",
]
