"""Base data structure for a register model item: map, register, field, etc."""

from __future__ import annotations

from abc import ABC
from pathlib import PurePath
from typing import TYPE_CHECKING, Any

from pydantic import BaseModel, ConfigDict, model_validator

from .types import IdentifierStr, SingleLineStr, TextStr

if TYPE_CHECKING:
    from typing_extensions import Self


class StrictModelItem(BaseModel, ABC):
    """Base data structure for a register model item: map, register, field, etc.

    This data structure designed to be as strict as possible:
    it is frozen (faux-immutable) and should have no defaults, so every field is assigned explicitly.

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
    def brief(self) -> SingleLineStr:
        """Brief description for an item, derived from `doc`.

        First line of `doc` is used.
        """
        return self._brief

    @property
    def description(self) -> TextStr:
        """Detailed description for in item, derived from `doc`.

        For a single-line `doc` it is the same as `brief`, but for multiline text block following brief is returned.
        """
        return self._description

    @property
    def parent(self) -> StrictModelItem:
        """Parent register model object."""
        return self._parent

    @property
    def path(self) -> PurePath:
        """Full path in object hierarchy. It is an abstract path very similar to real filesystem paths."""
        return self._path

    @model_validator(mode="after")
    def _init_brief(self) -> Self:
        """Initialize `brief` property."""
        self._brief = self.doc.split("\n", 1)[0].strip()
        return self

    @model_validator(mode="after")
    def _init_description(self) -> Self:
        """Initialize `description` property."""
        parts = self.doc.split("\n", 1)
        self._description = (parts[1] if len(parts) > 1 else parts[0]).strip()
        return self

    @model_validator(mode="after")
    def _init_path(self) -> Self:
        """Initialize `path` property."""
        if not hasattr(self, "_path"):
            self._path = PurePath(self.name)
        return self

    def _assign_parent(self, item: StrictModelItem) -> None:
        """Set `parent` property.

        This one-time method has to be used, because model is frozen and parent field is empty after creation.
        So it is the only way to update `parent` field.
        This method is typically called inside parent, when child is assigned during validation.
        """
        if not hasattr(self, "_parent"):
            self._parent = item
            self._path = self._parent.path / self._path

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
