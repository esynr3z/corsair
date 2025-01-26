"""Loader for serialized register maps (JSON, JSON5, YAML, etc.)."""

from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from .base import Loader, LoaderConfig

if TYPE_CHECKING:
    from corsair import Map


class SerializedLoader(Loader):
    """Load register map from serialized format (JSON, JSON5, YAML, etc.)."""

    class Config(LoaderConfig):
        """Configuration for the serialized loader."""

        kind: Literal["json", "yaml"]
        """Loader kind discriminator."""

    @classmethod
    def get_config_cls(cls) -> type[LoaderConfig]:
        """Get the configuration class for the loader."""
        return cls.Config

    def __call__(self) -> Map:
        """Load the register map from a module."""
        raise NotImplementedError
