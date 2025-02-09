"""Loader for register maps in Python modules."""

from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from .base import Loader, LoaderConfig

if TYPE_CHECKING:
    from corsair import Map


class PyModuleLoader(Loader):
    """Load register map from a Python module."""

    class Config(LoaderConfig):
        """Configuration for the Python module loader."""

        kind: Literal["py"]
        """Loader kind discriminator."""

    @classmethod
    def get_config_cls(cls) -> type[LoaderConfig]:
        """Get the configuration class for the loader."""
        return cls.Config

    def _load(self) -> Map:
        """Load the register map."""
        raise NotImplementedError
