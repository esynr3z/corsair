"""Build specification for a user project."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING

import yaml
from pydantic import BaseModel, ConfigDict, Field

from ._generators import AnyGeneratorConfig
from ._loaders import AnyLoaderConfig, SerializedLoader

if TYPE_CHECKING:
    from pathlib import Path


class BuildSpecification(BaseModel):
    """Specification that describes how to build everything."""

    loader: AnyLoaderConfig = SerializedLoader.Config(kind="yaml")
    """Configuration for the loader."""

    generators: dict[str, AnyGeneratorConfig] = Field(..., min_length=1)
    """Configuration for the generators to build all required files."""

    @classmethod
    def from_file(cls, path: Path) -> BuildSpecification:
        """Load specification from YAML file."""
        with path.open("r", encoding="utf-8") as f:
            return BuildSpecification(**yaml.safe_load(f))

    @classmethod
    def to_json_schema_file(cls, path: Path) -> None:
        """Write JSON schema to file."""
        with path.open("w") as f:
            schema = cls.model_json_schema()
            json.dump(schema, f)

    model_config = ConfigDict(
        extra="forbid",
        use_attribute_docstrings=True,
    )
