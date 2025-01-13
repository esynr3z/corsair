"""Build specification for a user project."""

from __future__ import annotations

import json
import sys
from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field

from ._generators import AnyGeneratorConfig
from ._parsers import AnyParserConfig, Deserializer

if sys.version_info >= (3, 11):
    import tomllib as tomlib
else:
    import tomli as tomlib

if TYPE_CHECKING:
    from pathlib import Path


class BuildSpecification(BaseModel):
    """Specification that describes how to build everything."""

    parser: AnyParserConfig = Deserializer.Config(kind="yaml")
    """Configuration for the parser."""

    generators: list[AnyGeneratorConfig] = Field(..., min_length=1)
    """Configuration for the generators to build all required files."""

    @classmethod
    def from_toml_file(cls, path: Path) -> BuildSpecification:
        """Load specification from TOML file."""
        with path.open("rb") as f:
            data = tomlib.load(f)
            return BuildSpecification(**data)

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
