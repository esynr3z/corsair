"""Build specification for a user project."""

from __future__ import annotations

import json
import sys
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

from pydantic import BaseModel, Field

from .config import GlobalConfig
from .target import AnyTarget

if sys.version_info >= (3, 11):
    import tomllib as tomlib
else:
    import tomli as tomlib


class BuildSpecification(BaseModel):
    """Specification that describes how to build everything."""

    config: GlobalConfig
    targets: dict[str, AnyTarget] = Field(description="Targets to build.")

    @staticmethod
    def from_toml_file(path: Path) -> BuildSpecification:
        """Load manifest from TOML file."""
        with path.open("rb") as f:
            data = tomlib.load(f)
            return BuildSpecification(**data)

    @staticmethod
    def to_json_schema_file(path: Path) -> None:
        """Load manifest from TOML file."""
        with path.open("w") as f:
            schema = BuildSpecification.model_json_schema()
            json.dump(schema, f)
