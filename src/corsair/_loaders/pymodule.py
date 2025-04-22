"""Loader for register maps in Python modules."""

from __future__ import annotations

from typing import Any, Literal

from .base import Loader, LoaderConfig


class PyModuleLoader(Loader):
    """Load register map from a Python module."""

    class Config(LoaderConfig):
        """Configuration for the Python module loader."""

        kind: Literal["py"] = "py"
        """Loader kind discriminator."""

        @property
        def loader_cls(self) -> type[Loader]:
            """Loader class to use."""
            return PyModuleLoader

        def get_kind(self) -> str:
            """Get the kind of the loader."""
            return self.kind

    @classmethod
    def get_config_cls(cls) -> type[LoaderConfig]:
        """Get the configuration class for the loader."""
        return cls.Config

    def _load_raw(self) -> dict[str, Any]:
        """Load the register map."""
        raise NotImplementedError
