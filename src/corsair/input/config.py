"""Configuration section of the build specification."""

from __future__ import annotations

from enum import Enum
from pathlib import Path

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    NonNegativeInt,
    PositiveInt,
    StrictBool,
)

from corsair import PyClassPathStr


class RegisterReset(str, Enum):
    """Flip-flop reset style."""

    SYNC_POS = "sync_pos"
    """Synchronous active high reset."""

    SYNC_NEG = "sync_neg"
    """Synchronous active low reset."""

    ASYNC_POS = "async_pos"
    """Asynchronous active high reset."""

    ASYNC_NEG = "async_neg"
    """Asynchronous active low reset."""


class GlobalConfig(BaseModel):
    """Global configuration parameters of the Corsair build specification."""

    regmap: Path = Path("csrmap.yaml")
    """Path to a register map to be processed."""

    regmap_parser: PyClassPathStr | None = Field(default=None, examples=["foo.py::FooParser"])
    """Select register map parser class explicitly.

    Parser is selected automatically based on file extension if value is not provided.
    """

    base_address: NonNegativeInt = 0
    """Register map base address in global address map."""

    data_width: PositiveInt = 32
    """Width of all data buses and registers (granularity of a register map)."""

    address_width: PositiveInt = 16
    """Address bus width (capacity of a register map)."""

    register_reset: RegisterReset = RegisterReset.SYNC_POS
    """Flip-flop reset style to be used in any generated HDL code."""

    address_increment: PositiveInt | StrictBool = False
    """Address auto increment mode.

    Address can be ommited for the most of registers, so this field controls how address is derived.
        * False - no auto increment
        * True - do auto increment based on `data_width` field
        * integer - do auto increment based on provided number of bytes
    """

    address_alignment: PositiveInt | StrictBool = True
    """Check for address alignment of registers.

        * False - no checks
        * True - do checks based on `data_width` field
        * integer - do checks based on provided number of bytes
    """

    model_config = ConfigDict(
        extra="allow",
        arbitrary_types_allowed=True,
        use_attribute_docstrings=True,
    )
