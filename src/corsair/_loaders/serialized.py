"""Loader for serialized register maps (JSON, HJSON, YAML)."""

from __future__ import annotations

import json
from typing import Any, Literal

import yaml

from .base import Loader, LoaderConfig


class SerializedLoader(Loader):
    """Load register map from serialized format (JSON, HJSON, YAML)."""

    class Config(LoaderConfig):
        """Configuration for the serialized loader."""

        kind: Literal["json", "yaml", "hjson"]
        """Loader kind discriminator."""

        @property
        def loader_cls(self) -> type[Loader]:
            """Related loader class."""
            return SerializedLoader

        def get_kind(self) -> str:
            """Get the kind of the loader."""
            return self.kind

    @classmethod
    def get_config_cls(cls) -> type[LoaderConfig]:
        """Get the configuration class for the loader."""
        return cls.Config

    def _load_raw(self) -> dict[str, Any]:
        """Load the register map."""
        assert isinstance(self.config, self.Config)  # noqa: S101, to help type checker

        if self.config.kind == "json":
            regmap = self._load_json()
        elif self.config.kind == "yaml":
            regmap = self._load_yaml()
        elif self.config.kind == "hjson":
            regmap = self._load_hjson()
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
