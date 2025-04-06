"""Base class for register map loaders."""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, ValidationError

from corsair._model import Map, stringify_model_errors
from corsair._types import PyAttrPathStr


class LoaderValidationError(Exception):
    """Raised when loader fails during data validation."""

    def __init__(self, pydantic_error: ValidationError, error_messages: list[str]) -> None:
        """Initialize the exception."""
        self.pydantic_error = pydantic_error
        self.error_messages = error_messages  # Store the stringified errors
        super().__init__("Loader failed during data validation")


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

    @property
    @abstractmethod
    def loader_cls(self) -> type[Loader]:
        """Related loader class."""


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
        self.raw_data: dict[str, Any] = {}

    def __call__(self) -> Map:
        """Load the register map."""
        if not isinstance(self.config, self.get_config_cls()):
            raise TypeError(
                f"Configuration instance is not of the expected type of "
                f"{self.__class__.__name__}.{self.get_config_cls().__name__}"
            )

        self.raw_data = self._load_raw()
        if self.config.overrides:
            self._apply_overrides(self.raw_data)

        try:
            return Map.model_validate(self.raw_data)
        except ValidationError as e:
            raise LoaderValidationError(e, stringify_model_errors(e, self.raw_data)) from e

    @abstractmethod
    def _load_raw(self) -> dict[str, Any]:
        """Load the register map into a dictionary, compatible with the `Map` model."""

    def _apply_overrides(self, raw_data: dict[str, Any]) -> None:
        """Apply overrides to the register map."""
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def get_config_cls(cls) -> type[LoaderConfig]:
        """Get the configuration class for the loader."""
