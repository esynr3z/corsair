"""Base class for register map loaders."""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict, ValidationError

from corsair._model import Map, stringify_model_errors


class LoaderValidationError(Exception):
    """Raised when loader fails during data validation."""

    def __init__(self, pydantic_error: ValidationError, error_messages: list[str]) -> None:
        """Initialize the exception."""
        self.pydantic_error = pydantic_error
        self.error_messages = error_messages  # Store the stringified errors
        super().__init__("Loader failed during data validation")

    def __str__(self) -> str:
        """Represent exception as a string."""
        err = "\n".join(self.error_messages)
        return f"{self.args[0]}\n{err}"


class LoaderConfig(BaseModel, ABC):
    """Base configuration for a loader."""

    mapfile: Path = Path("csrmap.yaml")
    """Path to the register map file."""

    model_config = ConfigDict(
        extra="forbid",
        use_attribute_docstrings=True,
    )

    @property
    @abstractmethod
    def loader_cls(self) -> type[Loader]:
        """Related loader class."""

    @abstractmethod
    def get_kind(self) -> str:
        """Get the kind of the loader."""


class Loader(ABC):
    """Base class for all register map loaders."""

    def __init__(self, config: LoaderConfig) -> None:
        """Initialize the loader."""
        self.config = config
        self.raw_data: dict[str, Any] = {}

        if not isinstance(self.config, self.get_config_cls()):
            raise TypeError(
                f"Configuration instance is not of the expected type of "
                f"{self.__class__.__name__}.{self.get_config_cls().__name__}"
            )

    def __call__(self) -> Map:
        """Load the register map."""
        if not self.config.mapfile.exists():
            raise FileNotFoundError(f"CSR map file not found: {self.config.mapfile}")

        self.raw_data = self._load_raw()

        try:
            return Map.model_validate(self.raw_data)
        except ValidationError as e:
            raise LoaderValidationError(e, stringify_model_errors(e, self.raw_data)) from e

    @abstractmethod
    def _load_raw(self) -> dict[str, Any]:
        """Load the register map into a dictionary, compatible with the `Map` model."""

    @classmethod
    @abstractmethod
    def get_config_cls(cls) -> type[LoaderConfig]:
        """Get the configuration class for the loader."""
