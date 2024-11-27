"""Internal representation of CSR."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import NonNegativeInt, PositiveInt, model_validator

from .field import Access, StrictField
from .item import StrictModelItem

if TYPE_CHECKING:
    from typing_extensions import Self


class StrictRegister(StrictModelItem):
    """Control and Status Register."""

    address: NonNegativeInt
    """Address value.

    This value represents an offset from the parent, which is `StrictMap` or `StrictBlock`.
    """

    width: PositiveInt
    """Bit width of a register including reserved (empty) bits. The value matches access bus data width."""

    fields: tuple[StrictField, ...]
    """Bit fields inside a register.

    Fields are sorted from LSB to MSB.
    """

    @property
    def access(self) -> Access:
        """Access mode based on access modes of the fields. Can only be RW, RO, WO."""
        return self._access

    @property
    def reset(self) -> NonNegativeInt:
        """Reset value based on reset values of the fields.

        Unknown reset value for a field converted to zero.
        """
        return self._reset

    @property
    def reset_binstr(self) -> str:
        """Reset value represented as a binary string where unknown bits masked as 'x'.

        No any prefix. Leading zeroes are added to match `width`.
        Examples: 00110, 1x10
        """
        return self._reset_binstr

    @property
    def reset_hexstr(self) -> str:
        """Reset value represented as a hexadecimal string where unknown nibbles masked as 'x'.

        No any prefix. Leading zeroes are added to match `width`.
        Examples: 0002bca, x2ax
        """
        return self._reset_hexstr

    @model_validator(mode="after")
    def check_fields_unique_names(self) -> Self:
        """Check that all field names inside register are unique."""
        names = [field.name for field in self.fields]
        duplicates = {name for name in names if names.count(name) > 1}
        if duplicates:
            raise ValueError(f"{self.path}: Some field names are not unique and used more than once: {duplicates}")
        return self

    @model_validator(mode="after")
    def check_fields_order(self) -> Self:
        """Check that all fields ordered from LSB to MSB."""
        for idx, field in enumerate(sorted(self.fields, key=lambda e: e.lsb)):
            if field != self.fields[idx]:
                order = (f"{f.name}.lsb={f.lsb}" for f in self.fields)
                raise ValueError(f"{self.path}: Fields has to be sorted by LSB: {', '.join(order)}")
        return self

    @model_validator(mode="after")
    def check_fields_overlapping(self) -> Self:
        """Check that no fields overlap other ones."""
        field_bits = {field.name: set(field.bit_indices) for field in self.fields}

        for field in self.fields:
            overlaps = {
                name: bool(set(field.bit_indices).intersection(bits))
                for name, bits in field_bits.items()
                if name != field.name
            }
            if any(v for v in overlaps.values()):
                raise ValueError(
                    f"{self.path}: Field {field.name} overlaps with other fields: {', '.join(overlaps.keys())}"
                )
        return self

    @model_validator(mode="after")
    def check_fields_width(self) -> Self:
        """Check that all fields fit register width."""
        last_field = self.fields[-1]
        if last_field.msb >= self.width:
            raise ValueError(
                f"{self.path}: Field {last_field.name} (lsb={last_field.lsb} msb={last_field.msb}) "
                f"exceeds size {self.width} of the register"
            )
        return self

    @model_validator(mode="after")
    def _init_access(self) -> Self:
        """Initialize `access` property."""
        if all(f.access.is_ro for f in self.fields):
            self._access = Access.RO
        elif all(f.access.is_wo for f in self.fields):
            self._access = Access.WO
        else:
            self._access = Access.RW
        return self

    @model_validator(mode="after")
    def _init_reset(self) -> Self:
        """Initialize `reset` property."""
        self._reset = 0
        for f in self.fields:
            self._reset |= (f.reset if f.reset else 0) << f.lsb
        return self

    @model_validator(mode="after")
    def _init_reset_binstr(self) -> Self:
        """Initialize `reset_binstr` property."""
        bits = ["0"] * self.width
        for f in self.fields:
            if f.reset:
                bits[f.lsb : f.msb + 1] = list(f"{f.reset:0{f.width}b}")
            else:
                bits[f.lsb : f.msb + 1] = ["x"] * f.width
        self._reset_binstr = "".join(reversed(bits))
        return self

    @model_validator(mode="after")
    def _init_reset_hexstr(self) -> Self:
        """Initialize `reset_hexstr` property."""
        nibbles = ["0"] * (self.width // 4)
        for i in range(len(nibbles)):
            bit_slice = self.reset_binstr[i * 4 : i * 4 + 4]
            if "x" in bit_slice:
                nibbles[i] = "x"
            else:
                nibbles[i] = f"{int(bit_slice):x}"
        self._reset_hexstr = "".join(reversed(nibbles))
        return self
