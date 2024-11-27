"""Internal representation of CSR field."""

from __future__ import annotations

import enum
from typing import TYPE_CHECKING

from pydantic import (
    NonNegativeInt,
    PositiveInt,
    model_validator,
)

from .enum import StrictEnum
from .item import StrictModelItem

if TYPE_CHECKING:
    from collections.abc import Iterable, Iterator

    from typing_extensions import Self


class Access(str, enum.Enum):
    """Access mode for a field.

    It is related to the bus accesses of the field and possible side-effects.
    """

    RW = "rw"
    """Read and Write. The field can be read or written."""

    RW1C = "rw1c"
    """Read and Write 1 to Clear. The field can be read, and when 1 is written field is cleared."""

    RW1S = "rw1s"
    """	Read and Write 1 to Set. The field can be read, and when 1 is written field is set."""

    RO = "ro"
    """Read Only. Write has no effect."""

    ROC = "roc"
    """Read Only to Clear. The field is cleared after every read."""

    ROLL = "roll"
    """Read Only + Latch Low. The field capture hardware active low pulse signal and stuck in 0.
    The field is set after every read."""

    ROLH = "rolh"
    """Read Only + Latch High. The field capture hardware active high pulse signal and stuck in 1.
    Read the field to clear it."""

    WO = "wo"
    """Write Only. Zeros are always read."""

    WOSC = "wosc"
    """Write Only + Self Clear. The field is cleared on the next clock tick after write."""

    def __str__(self) -> str:
        """Convert enumeration member into string."""
        return self.value

    @property
    def is_ro(self) -> bool:
        """Check that this access mode RO or its subset."""
        return self in (Access.RO, Access.ROC, Access.ROLH, Access.ROLL)

    @property
    def is_wo(self) -> bool:
        """Check that this access mode WO or its subset."""
        return self in (Access.WO, Access.WOSC)


class Hardware(str, enum.Flag):
    """Hardware mode for a field.

    Mode reflects hardware possibilities and interfaces to observe and modify bitfield value.
    """

    INPUT = "i"
    """Use input value from hardware to update the field."""

    I = INPUT
    """Shorthand for `INPUT`."""

    OUTPUT = "o"
    """Enable output value from the field to be accessed by hardware."""

    O = OUTPUT
    """Shorthand for `OUTPUT`."""

    CLEAR = "c"
    """Add signal to clear the field (fill with all zeros)."""

    C = CLEAR
    """Shorthand for `CLEAR`."""

    SET = "s"
    """Add signal to set the field (fill with all ones)."""

    S = SET
    """Shorthand for `SET`."""

    ENABLE = "e"
    """Add signal to enable the field to capture input value (must be used with `INPUT`)."""

    E = ENABLE

    LOCK = "l"
    """Add signal to lock the field (to prevent any changes)."""

    L = LOCK
    """Shorthand for `LOCK`."""

    ACCESS = "a"
    """Add signals to notify when bus access to the field is performed (at the same cycle)."""

    A = ACCESS
    """Shorthand for `ACCESS`."""

    QUEUE = "q"
    """Add simple interface to external queue (LIFO, FIFO)."""

    Q = QUEUE
    """Shorthand for `QUEUE`."""

    FIXED = "f"
    """Enable fixed mode (field is a constant)."""

    F = FIXED
    """Shorthand for `FIXED`."""

    NA = "n"
    """Not accessible by hardware."""

    N = NA
    """Shorthand for `NA`"""

    # Override original type hints to match actually used type
    value: str  # pyright: ignore [reportIncompatibleMethodOverride]
    _value_: str  # pyright: ignore [reportIncompatibleVariableOverride]

    @classmethod
    def _missing_(cls, value: object) -> enum.Enum:
        """Return member if one can be found for value, otherwise create a composite member.

        Composite member is created only iff value contains only members, else `ValueError` is raised.
        Based on `enum.Flag._create_pseudo_member_()` and `enum._decompose()`.
        """
        if not isinstance(value, str):
            raise TypeError(f"Member value has to be 'str', but {type(value)} is provided")
        if value == "":
            value = "n"  # Empty literal considered as 'n'
        value = value.lower()

        # Lookup for already created members (all members are singletons)
        member = cls._value2member_map_.get(value, None)
        if member is not None:
            return member

        # Create composite member
        flags = tuple(cls._split_flags(value))  # Can raise ValueError for unknown flags
        composite = str.__new__(cls)
        # Name style is the same as in `enum.Flag.__str__`
        composite._name_ = "|".join(
            [
                member._name_
                for member in cls  # Use iteration to follow order of declaration, rather than provided flags order
                if member._value_ in flags and member._name_
            ]
        )
        composite._value_ = cls._join_flags(flags)

        # Use setdefault in case another thread already created a composite with this value
        return cls._value2member_map_.setdefault(value, composite)

    @classmethod
    def _split_flags(cls, value: str) -> Iterator[str]:
        """Split string into flag values."""
        # For legacy reasons there could be a string without separators, where all flags are single chars.
        # Code below allows "ioe" and "i-o-e" as well.
        raw_flags = set(value.split("-") if "-" in value else value)

        # Collect all known flags in order of declaration
        self_flags = [member._value_ for member in cls]

        # Check that all raw flags are valid values
        for flag in raw_flags:
            if flag not in self_flags:
                raise ValueError(f"Unknown hardware mode {flag!r}")

        # Then generate flags in delaration order
        for member in cls:
            if member._value_ in raw_flags:
                yield member._value_

    @classmethod
    def _join_flags(cls, flags: Iterable[str]) -> str:
        """Concatenate all flag values into single string."""
        # For input strings flags without separators are allowed (refer to `_split_flags`),
        # but all other representations always use separators.
        return "-".join(flags)

    def __len__(self) -> int:
        """Return number of combined flags."""
        return sum(1 for _ in self)

    def __repr__(self) -> str:
        """Represent flags as a string in the same style as in `enum.Flag.__repr__()`."""
        return f"<{self.__class__.__name__}.{self._name_}: {self._value_!r}>"

    def __str__(self) -> str:
        """Represent flags as a compact string."""
        return self._value_

    def __or__(self, other: Self) -> Self:
        """Override `|` operator to combine flags into composite one."""
        cls = self.__class__
        if not isinstance(other, cls):
            raise TypeError(f"Can't OR {type(self)} with {type(other)}")
        return cls(cls._join_flags((self._value_, other._value_)))

    def __contains__(self, item: object) -> bool:
        """Overload `in` operator to check flag inclusions."""
        cls = self.__class__
        if isinstance(item, str):
            item = cls(item)
        if not isinstance(item, cls):
            raise TypeError(f"Can't use `in` for {type(self)} with {type(item)}")
        self_flags = tuple(cls._split_flags(self._value_))
        return all(flag in self_flags for flag in cls._split_flags(item._value_))

    def __iter__(self) -> Iterator[Self]:
        """Iterate over combination of flags."""
        cls = self.__class__
        for flag in cls._split_flags(self._value_):
            yield cls(flag)

    def __le__(self, other: object) -> bool:
        """Overload `<=` operator to check if current flags are the same or the subset of other."""
        cls = self.__class__
        if isinstance(other, str):
            other = cls(other)
        if not isinstance(other, cls):
            raise TypeError(f"Can't compare {type(self)} with {type(other)}")
        return self in other

    def __ge__(self, other: object) -> bool:
        """Overload `>=` operator to check if current flags are the same or the superset of other."""
        cls = self.__class__
        if isinstance(other, str):
            other = cls(other)
        if not isinstance(other, cls):
            raise TypeError(f"Can't compare {type(self)} with {type(other)}")
        return other in self

    def __lt__(self, other: object) -> bool:
        """Overload `<` operator to check if current flags are the subset of other."""
        cls = self.__class__
        if isinstance(other, str):
            other = cls(other)
        if not isinstance(other, cls):
            raise TypeError(f"Can't compare {type(self)} with {type(other)}")
        return self._value_ != other._value_ and self.__le__(other)

    def __gt__(self, other: object) -> bool:
        """Overload `>` operator to check if current flags are the superset of other."""
        cls = self.__class__
        if isinstance(other, str):
            other = cls(other)
        if not isinstance(other, cls):
            raise TypeError(f"Can't compare {type(self)} with {type(other)}")
        return self._value_ != other._value_ and self.__ge__(other)


class StrictField(StrictModelItem):
    """Bit field inside a register."""

    reset: NonNegativeInt | None
    """Reset value. Can be unknown."""

    width: PositiveInt
    """Bit width."""

    offset: NonNegativeInt
    """Bit offset within register."""

    access: Access
    """Access mode."""

    hardware: Hardware
    """Hardware interaction options."""

    enum: StrictEnum | None
    """Optional enumeration for the field."""

    @property
    def bit_indices(self) -> Iterator[int]:
        """Iterate over field bit positions inside register from LSB to MSB."""
        yield from range(self.offset, self.offset + self.width)

    @property
    def byte_indices(self) -> Iterator[int]:
        """Iterate over field byte indices inside register from lower to higher."""
        yield from range(self.offset // 8, (self.offset + self.width - 1) // 8 + 1)

    @property
    def lsb(self) -> int:
        """Position of the least significant bit (LSB) inside register."""
        return self.offset

    @property
    def msb(self) -> int:
        """Position of the most significant bit (MSB) inside register."""
        return self.lsb + self.width - 1

    @property
    def mask(self) -> int:
        """Bit mask for the bitfield inside register."""
        return (2 ** (self.width) - 1) << self.offset

    @property
    def is_multibit(self) -> bool:
        """Bitfield has more than one bit width."""
        return self.width > 1

    def byte_select(self, byte_idx: int) -> tuple[int, int]:
        """Return register bit slice infomation (MSB, LSB) for a field projection into Nth byte of a register.

        This method facilitates organization of "byte select" logic within HDL templates.

        Example for `offset=3` and `width=7` bitfield:

        ```
                           6     3     0  <-- field bits
                           |     |     |
        field:             1 1 1 1 1 1 1
        reg:   0 0 0 0 0 0 1 1 1 1 1 1 1 0 0 0
               |    byte 1     |   byte 0    |
               15              7             0  <-- register bits
        ```

        For `byte_idx=0` result is `(7, 3)`, for `byte_idx=1` -- `(9, 8)`
        """
        byte_indices = tuple(self.byte_indices)
        if byte_idx not in byte_indices:
            raise ValueError(f"Provided {byte_idx=} has to be one of {byte_indices} for the field.")

        lsb = self.lsb if byte_idx == byte_indices[0] else byte_idx * 8
        msb = (byte_idx + 1) * 8 - 1 if ((byte_idx + 1) * 8 - 1 - self.msb) < 0 else self.msb

        return (msb, lsb)

    def byte_select_self(self, byte_idx: int) -> tuple[int, int]:
        """Return field bit slice infomation for field projection into Nth byte of a register.

        Refer to `byte_select` to get the idea. The only difference is
        that current method returns non-offsetted bit slice to represent positions within bitfield itself.
        """
        msb, lsb = self.byte_select(byte_idx)
        return (msb - self.offset, lsb - self.offset)

    @model_validator(mode="after")
    def _check_hardware_constraints(self) -> Self:
        """Check that `hardware` field follows expected constraints."""
        # Check exclusive hardware flags
        for flag in (Hardware.NA, Hardware.QUEUE, Hardware.FIXED):
            if flag in self.hardware and len(self.hardware) > 1:
                raise ValueError(f"Hardware mode '{flag}' must be exclusive, but current mode is '{self.hardware}'")

        # Hardware queue mode can be only combined with specific access values
        if Hardware.QUEUE in self.hardware:
            q_access_allowed = [Access.RW, Access.RO, Access.WO]
            if self.access not in q_access_allowed:
                raise ValueError(
                    f"Hardware mode 'q' is allowed to use only with '{q_access_allowed}', "
                    f"but current access mode is '{self.access}'"
                )

        # Enable must be used with Input
        if Hardware.ENABLE in self.hardware and Hardware.INPUT not in self.hardware:
            raise ValueError(
                f"Hardware mode 'e' is allowed to use only with 'i', " f"but current hardware mode is '{self.hardware}'"
            )
        return self

    @model_validator(mode="after")
    def _check_reset_width(self) -> Self:
        """Check that reset value width less or equal field width."""
        if self.reset:
            reset_value_width = self.reset.bit_length()
            if reset_value_width > self.width:
                raise ValueError(
                    f"Reset value 0x{self.reset:x} requires {reset_value_width} bits to represent,"
                    f" but field is {self.width} bits wide"
                )
        return self

    @model_validator(mode="after")
    def _check_enum_members_width(self) -> Self:
        """Check that enumeration members has values, which width fit field width."""
        if self.enum and self.enum.width > self.width:
            raise ValueError(
                f"Enumeration {self.enum} requires {self.enum.width} bits to represent,"
                f" but field is {self.width} bits wide"
            )
        return self

    @model_validator(mode="after")
    def _update_refs(self) -> Self:
        """Update references to parent in all child items."""
        if self.enum:
            self.enum._assign_parent(self)  # noqa: SLF001
        return self
