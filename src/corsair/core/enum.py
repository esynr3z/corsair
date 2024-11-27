"""Internal representation of CSR field enumeration."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import NonNegativeInt, model_validator

from .item import StrictModelItem

if TYPE_CHECKING:
    from collections.abc import Iterator

    from typing_extensions import Self

    from .types import IdentifierStr


class StrictEnumMember(StrictModelItem):
    """Member of a bit field enumeration."""

    value: NonNegativeInt
    """Enumeration value."""

    @property
    def width(self) -> NonNegativeInt:
        """Number of bits required to represent the value."""
        return self._width

    @model_validator(mode="after")
    def _init_width(self) -> Self:
        """Initialize `width` property."""
        self._width = self.value.bit_length()
        if self._width == 0:
            self._width = 1  # bit_length() returns zero for zero value, so assign minimum value
        return self


class StrictEnum(StrictModelItem):
    """Enumeration of a bit field."""

    members: tuple[StrictEnumMember, ...]
    """Enumeration members.

    Members are sorted by value in ascending order.
    """

    @property
    def width(self) -> NonNegativeInt:
        """Number of bits required to represent the largest member of enumeration."""
        return self._width

    @property
    def names(self) -> Iterator[IdentifierStr]:
        """Iterate over names of members."""
        return (m.name for m in self.members)

    @property
    def values(self) -> Iterator[NonNegativeInt]:
        """Iterate over values of members."""
        return (m.value for m in self.members)

    @model_validator(mode="after")
    def _check_enum_unique_values(self) -> Self:
        """Check that all values inside enumeration are unique."""
        if len({member.value for member in self.members}) != len(self.members):
            raise ValueError(f"Some enumeration member values are not unique: {self.members}")
        return self

    @model_validator(mode="after")
    def _check_enum_unique_names(self) -> Self:
        """Check that all names inside enumeration are unique."""
        if len({member.name for member in self.members}) != len(self.members):
            raise ValueError(f"Some enumeration member names are not unique: {self.members}")
        return self

    @model_validator(mode="after")
    def _check_enum_members_order(self) -> Self:
        """Check that all enum members are sorted by value."""
        for idx, member in enumerate(sorted(self.members, key=lambda e: e.value)):
            if member != self.members[idx]:
                raise ValueError(f"Enumeration members has to be sorted by value: {self.members}")
        return self

    @model_validator(mode="after")
    def _init_width(self) -> Self:
        """Initialize `width` property."""
        self._width = max(m.width for m in self.members)
        return self

    @model_validator(mode="after")
    def _update_refs(self) -> Self:
        """Update references to parent in all child items."""
        for m in self.members:
            m._assign_parent(self)  # noqa: SLF001
        return self
