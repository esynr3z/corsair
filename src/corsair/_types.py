"""Common types used in most classes and data models."""

from __future__ import annotations

from typing import Annotated

from pydantic import AfterValidator, StringConstraints

IdentifierStr = Annotated[
    str,
    StringConstraints(
        to_lower=True,
        strip_whitespace=True,
        min_length=1,
        pattern=r"^[A-Za-z_][A-Za-z0-9_]*$",
    ),
]
"""A lowercase string that represents a valid identifier/name."""

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


def _is_power_of_two(value: int) -> int:
    """Check if a number is a power of two."""
    if not (value > 0 and (value & (value - 1)) == 0):
        raise ValueError(f"Value {value} is not a power of two")
    return value


Pow2Int = Annotated[int, AfterValidator(_is_power_of_two)]
"""An integer that is a power of two."""
