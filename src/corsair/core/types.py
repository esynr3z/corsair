"""Common types used in most classes and data models."""

from __future__ import annotations

from typing import Annotated

from pydantic import (
    NonNegativeInt,
    StringConstraints,
    TypeAdapter,
)

IdentifierStr = Annotated[
    str,
    StringConstraints(
        to_lower=True,
        strip_whitespace=True,
        min_length=1,
        pattern=r"^[A-Za-z_][A-Za-z0-9_]*$",
    ),
]
"""A string that represents a valid identifier/name."""

SingleLineStr = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        pattern=r"^[^\n\r]*$",
    ),
]
"""A string that represents a single line text."""

TextStr = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
    ),
]
"""A string that represent a generic text (can be multiline)."""

PyClassPathStr = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        pattern=r"^.+\.py::[A-Za-z0-9_]+$",
    ),
]
"""A string that represents a path to a class within some python file."""


non_negative_int_adapter = TypeAdapter(NonNegativeInt)
"""Type adapter for `NonNegativeInt` type to validation of objects of that type."""
