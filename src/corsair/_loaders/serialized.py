"""Loader for serialized register maps (JSON, HJSON, TOML, YAML)."""

from __future__ import annotations

import json
import sys
from typing import Any, Literal

import yaml

if sys.version_info >= (3, 11):
    import tomllib as tomlib
else:
    import tomli as tomlib

from .base import Loader, LoaderConfig


class SerializedLoader(Loader):
    """Load register map from serialized format (JSON, HJSON, TOML, YAML)."""

    class Config(LoaderConfig):
        """Configuration for the serialized loader."""

        kind: Literal["json", "yaml", "hjson", "toml"]
        """Loader kind discriminator."""

        @property
        def loader_cls(self) -> type[Loader]:
            """Related loader class."""
            return SerializedLoader

    @classmethod
    def get_config_cls(cls) -> type[LoaderConfig]:
        """Get the configuration class for the loader."""
        return cls.Config

    def _load_raw(self) -> dict[str, Any]:
        """Load the register map."""
        if not isinstance(self.config, self.Config):
            raise TypeError("Configuration instance is not of the expected type of SerializedLoader.Config")

        if not self.config.mapfile.exists():
            raise FileNotFoundError(f"File not found: {self.config.mapfile}")

        if self.config.kind == "json":
            regmap = self._load_json()
        elif self.config.kind == "yaml":
            regmap = self._load_yaml()
        elif self.config.kind == "hjson":
            regmap = self._load_hjson()
        elif self.config.kind == "toml":
            regmap = self._load_toml()
        else:
            raise ValueError(f"Invalid kind: {self.config.kind}")

        return regmap

    def _load_json(self) -> dict[str, Any]:
        """Load the register map from a JSON file."""
        with self.config.mapfile.open("r", encoding="utf-8") as file:
            return json.load(file)

    def _load_yaml(self) -> dict[str, Any]:
        """Load the register map from a YAML file."""
        with self.config.mapfile.open("r", encoding="utf-8") as file:
            return yaml.safe_load(file)

    def _load_hjson(self) -> dict[str, Any]:
        """Load the register map from a HJSON file."""
        try:
            import hjson  # type: ignore reportMissingImports
        except ImportError as e:
            raise ImportError(
                "hjson is not installed. "
                "Try installing it with `pip install corsair[hjson]` or `pip install corsair[full]`."
            ) from e

        with self.config.mapfile.open("r", encoding="utf-8") as file:
            return hjson.load(file)

    def _load_toml(self) -> dict[str, Any]:
        """Load the register map from a TOML file."""
        with self.config.mapfile.open("rb") as file:
            return tomlib.load(file)
