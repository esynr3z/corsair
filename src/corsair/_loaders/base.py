"""Base class for register map loaders."""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import TYPE_CHECKING, Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from corsair._types import PyAttrPathStr

if TYPE_CHECKING:
    from corsair._model import Map


class LoaderConfig(BaseModel, ABC):
    """Base configuration for a loader."""

    mapfile: Path = Path("csrmap.yaml")
    """Path to the register map file."""

    overrides: dict[str, Any] = {}
    """Overrides to apply to the register map."""

    model_config = ConfigDict(
        extra="forbid",
        use_attribute_docstrings=True,
    )


class CustomLoaderConfig(LoaderConfig):
    """Custom configuration that is used by custom loader class."""

    kind: Literal["custom"]
    """Loader kind discriminator."""

    loader: PyAttrPathStr = Field(..., examples=["bar.py::BarLoader"])
    """Path to a custom loader class to be used."""

    model_config = ConfigDict(
        extra="allow",
        use_attribute_docstrings=True,
    )

    @property
    def loader_cls(self) -> type[Loader]:
        """Loader class to use."""
        # TODO: implement dynamic loading of loader class
        raise NotImplementedError


class Loader(ABC):
    """Base class for all register map loaders."""

    def __init__(self, config: LoaderConfig) -> None:
        """Initialize the loader."""
        self.config = config

    def __call__(self) -> Map:
        """Load the register map."""
        if not isinstance(self.config, self.get_config_cls()):
            raise TypeError(
                f"Configuration instance is not of the expected type of "
                f"{self.__class__.__name__}.{self.get_config_cls().__name__}"
            )

        regmap = self._load()
        if self.config.overrides:
            self._apply_overrides(regmap)

        return regmap

    @abstractmethod
    def _load(self) -> Map:
        """Load the register map."""

    def _apply_overrides(self, regmap: Map) -> None:
        """Apply overrides to the register map."""
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def get_config_cls(cls) -> type[LoaderConfig]:
        """Get the configuration class for the loader."""
