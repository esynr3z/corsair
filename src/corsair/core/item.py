"""Base strict model to encapsulate common fields for any register map item."""

from __future__ import annotations

from abc import ABC
from typing import Any

from pydantic import BaseModel, ConfigDict

from .types import IdentifierStr, TextStr


class StrictBaseItem(BaseModel, ABC):
    """Base strict model for a register map item.

    This is a strict immutable internal representation to be used with output generators:

    * it is frozen (immutable)
    * has no defaults and no no optional fields
    * not adapted for getting pretty dump and schema

    This allows to provide more solid contract for generators,
    when all fields are filled, validated, available and immutable.
    """

    name: IdentifierStr
    """Name of an item."""

    doc: TextStr
    """Docstring for an item.

    Follows Python docstring rules - first line is a brief summary,
    then optionally, empty line following detailed description.
    """

    metadata: dict[str, Any]
    """Additional user metadata attached to an item."""

    @property
    def brief(self) -> str:
        """Brief description for an item, extracted from `doc`.

        First line of `doc` is used.
        """
        return self.doc.split("\n", 1)[0].strip()

    @property
    def description(self) -> str:
        """Detailed description for in item, extracted from `doc`.

        For a single-line `doc` it is the same as `brief`, but for multiline text block following brief is returned.
        """
        parts = self.doc.split("\n", 1)
        return (parts[1] if len(parts) > 1 else parts[0]).strip()

    model_config = ConfigDict(
        # Docstrings of attributesshould be used for field descriptions
        use_attribute_docstrings=True,
        # Model is faux-immutable
        frozen=True,
        # Strict validation (no coercion) is applied to all fields on the model
        strict=True,
        # Extra values are not permitted
        extra="forbid",
    )
