"""Base classes for all generators."""

from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum
from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    from collections.abc import Iterator
    from pathlib import Path

    from corsair._model import Map

from pydantic import BaseModel, ConfigDict, Field, ValidationInfo, field_validator

from corsair._types import IdentifierStr, PyClassPathStr


class GeneratorConfig(BaseModel, ABC):
    """Base configuration for a generator."""

    label: IdentifierStr = ""
    """Unique label of the generator."""

    use_map: str
    """Name of the map to use for the generation."""

    model_config = ConfigDict(
        extra="allow",
        use_attribute_docstrings=True,
    )

    @field_validator("label")
    @classmethod
    def _derive_label(cls, v: str, info: ValidationInfo) -> str:
        """Derive the label from the generator kind."""
        if v == "":
            v = info.data.get("kind", "").lower()
        return v


class CustomGeneratorConfig(GeneratorConfig):
    """Custom configuration that is used by custom generator class."""

    kind: Literal["custom"]
    """Generator kind discriminator."""

    generator: PyClassPathStr = Field(..., examples=["bar.py::BarGenerator"])
    """Path to a custom generator class to be used."""

    @property
    def generator_cls(self) -> type[Generator]:
        """Generator class to use."""
        # TODO: implement dynamic loading of generator class
        raise NotImplementedError


class Generator(ABC):
    """Base class for all generators."""

    def __init__(self, register_map: Map, config: GeneratorConfig) -> None:
        """Initialize the generator."""
        self.register_map = register_map
        self.config = config

    @abstractmethod
    def __call__(self, output_dir: Path, dry_run: bool = False) -> Iterator[Path]:
        """Generate all the outputs."""

    @classmethod
    @abstractmethod
    def get_config_cls(cls) -> type[GeneratorConfig]:
        """Get the configuration class for the generator."""


class ResetStyle(str, Enum):
    """Flip-flop reset style."""

    SYNC_POS = "sync_pos"
    """Synchronous active high reset."""

    SYNC_NEG = "sync_neg"
    """Synchronous active low reset."""

    ASYNC_POS = "async_pos"
    """Asynchronous active high reset."""

    ASYNC_NEG = "async_neg"
    """Asynchronous active low reset."""
