"""Base class for register map parsers."""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import TYPE_CHECKING, Literal

from pydantic import BaseModel, ConfigDict, Field

from corsair._types import PyClassPathStr

if TYPE_CHECKING:
    from collections.abc import Iterator

    from corsair._model import Map


class ParserConfig(BaseModel, ABC):
    """Base configuration for a parser."""

    mapfile: Path
    """Path to the register map file to parse."""

    model_config = ConfigDict(
        extra="allow",
        use_attribute_docstrings=True,
    )


class CustomParserConfig(ParserConfig):
    """Custom configuration that is used by custom parser class."""

    kind: Literal["custom"]
    """Parser kind discriminator."""

    parser: PyClassPathStr = Field(..., examples=["bar.py::BarParser"])
    """Path to a custom parser class to be used."""

    @property
    def parser_cls(self) -> type[Parser]:
        """Parser class to use."""
        # TODO: implement dynamic loading of parser class
        raise NotImplementedError


class Parser(ABC):
    """Base class for all parsers."""

    def __init__(self, config: ParserConfig) -> None:
        """Initialize the parser."""
        self.config = config

    @abstractmethod
    def __call__(self) -> Iterator[Map]:
        """Parse the register map."""

    @classmethod
    @abstractmethod
    def get_config_cls(cls) -> type[ParserConfig]:
        """Get the configuration class for the parser."""
