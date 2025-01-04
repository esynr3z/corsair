"""Internal register model."""

from __future__ import annotations

import enum
import math
from abc import ABC, abstractmethod
from collections import defaultdict
from pathlib import PurePath
from typing import TYPE_CHECKING

from pydantic import (
    BaseModel,
    ConfigDict,
    ValidationInfo,
    field_validator,
    model_validator,
)
from pydantic.types import NonNegativeInt, PositiveInt

from ._types import IdentifierStr, Pow2Int, SingleLineStr, TextStr

if TYPE_CHECKING:
    from collections.abc import Iterable, Iterator

    from typing_extensions import Self

__all__ = (
    "AccessMode",
    "AccessCategory",
    "MemoryStyle",
    "HardwareMode",
    "Metadata",
    "Item",
    "MapableItem",
    "ArrayItem",
    "EnumMember",
    "Enum",
    "Field",
    "Register",
    "Memory",
    "Map",
    "FieldArray",
    "RegisterArray",
    "MemoryArray",
    "MapArray",
)


class AccessMode(str, enum.Enum):
    """Access mode for a field.

    It describes how the field can be accessed by bus/software and possible side-effects.
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
    def category(self) -> AccessCategory:
        """Access category."""
        if self in (AccessMode.RO, AccessMode.ROC, AccessMode.ROLH, AccessMode.ROLL):
            return AccessCategory.RO
        if self in (AccessMode.WO, AccessMode.WOSC):
            return AccessCategory.WO
        if self == AccessMode.RW:
            return AccessCategory.RW
        raise ValueError(f"Cannot map access mode {self} to any category")

    @property
    def is_ro(self) -> bool:
        """Check that this access mode belongs to RO category."""
        return self.category == AccessCategory.RO

    @property
    def is_wo(self) -> bool:
        """Check that this access mode belongs to WO category."""
        return self.category == AccessCategory.WO

    @property
    def is_rw(self) -> bool:
        """Check that this access mode belongs to RW category."""
        return self.category == AccessCategory.RW


class AccessCategory(str, enum.Enum):
    """Common access categories every `Access` mode belongs to."""

    RW = AccessMode.RW
    """Read and Write. The field can be read or written."""

    RO = AccessMode.RO
    """Read Only. Write has no effect."""

    WO = AccessMode.WO
    """Write Only. Read returns zeros."""

    def __str__(self) -> str:
        """Convert enumeration member into string."""
        return self.value


class MemoryStyle(str, enum.Enum):
    """Memory block implementation style for `Memory`."""

    INTERNAL_RO = "internal_ro"
    """Memory block is implemented inside CSR map RTL module.
    It can be read from bus and can be written to by hardware.
    """

    INTERNAL_CONST = "internal_const"
    """Memory block is implemented inside CSR map RTL module.
    It filled with constants that can be read from bus only.
    """

    INTERNAL_WO = "internal_wo"
    """Memory block is implemented inside CSR map RTL module.
    It can be written to by bus and can be read by hardware.
    """

    INTERNAL_RW = "internal_rw"
    """Memory block is implemented inside CSR map RTL module.
    It can be read from bus and can be written to by bus only.
    """

    EXTERNAL_RO = "external_ro"
    """Memory block is implemented outside CSR map RTL module.
    It can be read from bus by read port within interface.
    """

    EXTERNAL_WO = "external_wo"
    """Memory block is implemented outside CSR map RTL module.
    It can be written to by bus by write port within interface.
    """

    EXTERNAL_RW = "external_rw"
    """Memory block is implemented outside CSR map RTL module.
    It can be read and written from bus by read and write ports within interface.
    """

    def __str__(self) -> str:
        """Convert enumeration member into string."""
        return self.value

    @property
    def access(self) -> AccessCategory:
        """Access category."""
        if "ro" in self.value:
            return AccessCategory.RO
        if "wo" in self.value:
            return AccessCategory.WO
        if "rw" in self.value:
            return AccessCategory.RW
        raise ValueError(f"Cannot map memory style {self} to any access category")

    @property
    def is_ro(self) -> bool:
        """Check that this access mode belongs to RO category."""
        return self.access == AccessCategory.RO

    @property
    def is_wo(self) -> bool:
        """Check that this access mode belongs to WO category."""
        return self.access == AccessCategory.WO

    @property
    def is_rw(self) -> bool:
        """Check that this access mode belongs to RW category."""
        return self.access == AccessCategory.RW


class HardwareMode(str, enum.Flag):
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

        # Then generate flags in declaration order
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


class Metadata(BaseModel):
    """Metadata for an item."""

    # All fields are created by user

    model_config = ConfigDict(
        # Model is faux-immutable
        frozen=True,
        # Extra values are allowed
        extra="allow",
    )


class Item(BaseModel, ABC):
    """Base data structure for all CSR model internal items: map, register, field, etc.

    Its strictness and immutability allows to provide solid contract for generators, when they traverse the model.
    Immutability also allows to cache properties to avoid recalculations and use model hashing.

    This class provides basic functionality to differentiate an item from other items
    and understand its place in the hierarchy.
    """

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

    name: IdentifierStr
    """Name of an item."""

    doc: TextStr
    """Docstring for an item.

    Follows Python docstring rules - first line is a brief summary,
    then optionally, empty line following detailed multiline description.
    """

    metadata: Metadata = Metadata()
    """Optional user metadata attached to an item."""

    @property
    def brief(self) -> SingleLineStr:
        """Brief description for an item, derived from `doc`.

        First line of `doc` is used.
        """
        if not hasattr(self, "_brief"):  # caching is ok - model is frozen
            self._brief = self.doc.split("\n", 1)[0].strip()
        return self._brief

    @property
    def description(self) -> TextStr:
        """Detailed description for in item, derived from `doc`.

        For a single-line `doc` it is the same as `brief`, but for multiline text block following brief is returned.
        """
        if not hasattr(self, "_description"):
            parts = self.doc.split("\n", 1)
            self._description = (parts[1] if len(parts) > 1 else parts[0]).strip()
        return self._description

    @property
    def parent(self) -> Item:
        """Parent for register model item."""
        if not hasattr(self, "_parent"):
            msg = self._err_fmt("Parent is not set")
            raise AttributeError(msg)
        return self._parent

    @property
    def path(self) -> PurePath:
        """Full path in object hierarchy. It is an abstract path very similar to real filesystem paths."""
        if not hasattr(self, "_path"):
            self._path = PurePath(self.name)
        return self._path

    def _err_fmt(self, message: str) -> str:
        """Format error message properly."""
        return f"{self.path}: {message}"

    def _assign_parent(self, item: Item) -> None:
        """Set `parent` property.

        This one-time method has to be used, because model is frozen and parent field is empty after creation.
        So it is the only way to update `parent` field.
        This method is typically called inside parent, when child is assigned during validation.
        """
        if not hasattr(self, "_parent"):
            self._parent = item
            self._path = self._parent.path / self.path

    @model_validator(mode="after")
    @abstractmethod
    def _update_backlinks(self) -> Self:
        """Update backlinks to current parent in all child items."""


class MapableItem(Item):
    """Item that can be mappend into global address space.

    This class add properties to work with address space and get address of the item.
    """

    offset: NonNegativeInt
    """Byte offset from the parent addressable item."""

    @property
    def base_address(self) -> NonNegativeInt:
        """Address, which this item is offsetted from."""
        if not hasattr(self, "_base_address"):
            if not hasattr(self, "_parent") or not isinstance(self.parent, MapableItem):
                self._base_address = 0
            else:
                self._base_address = self.parent.address
        return self._base_address

    @property
    def address(self) -> NonNegativeInt:
        """Global address of the item."""
        if not hasattr(self, "_address"):
            self._address = self.base_address + self.offset
        return self._address

    @property
    @abstractmethod
    def _offset_alignment(self) -> Pow2Int:
        """Number of bytes `offset` has to be aligned to."""

    @model_validator(mode="after")
    def _check_offset_alignment(self) -> Self:
        """Check that offset is properly aligned."""
        if self.offset & (self._offset_alignment - 1):
            msg = self._err_fmt(
                f"Address offset 0x{self.offset:x} is not aligned "
                f"to expected value of {self._offset_alignment} bytes"
            )
            raise ValueError(msg)
        return self


class ArrayItem(Item):
    """Item that can describe array of items with common properties following some repeatable pattern."""

    num: PositiveInt
    """Number of elements within the array."""

    increment: PositiveInt
    """Offset increment for each array element."""

    indices: tuple[str, ...] = ()
    """Unique index (label) for each array element.

    Index can be numeric (0, 1, 2, ...), alphabetic (a, b, c, ...), or any string.
    If indices are not provided (empty tuple), they will be generated as numeric (0, 1, 2, ...) based on `num`.

    Number of indices should be greater or equal to `num`.
    """

    naming: str = "{name}{index}"
    """Pattern for element name.

    The pattern can use `{name}` and `{index}` placeholders to insert `name` and concrete index into the name.
    `{name}` can be omitted, but `{index}` is required.

    Examples:
    - `{name}{index}` -> `gpioa`, `gpiob`, `gpioc`, ...
    - `{name}_{index}` -> `irq0`, `irq1`, `irq2`, ...
    """

    @property
    def generated_items(self) -> tuple[Item, ...]:
        """Concrete items in array created by following the pattern."""
        if not hasattr(self, "_generated_items"):
            self._generated_items = self._generate_items()
        return self._generated_items

    @abstractmethod
    def _generate_items(self) -> tuple[Item, ...]:
        """Generate concrete items in the array."""

    @field_validator("indices", mode="after")
    @classmethod
    def _fill_indices(cls, values: tuple[str, ...], info: ValidationInfo) -> tuple[str, ...]:
        """Fill indices with numeric values if they are not provided."""
        if not values:
            return tuple(str(i) for i in range(info.data["num"]))
        return values

    @model_validator(mode="after")
    def _check_minimum_num(self) -> Self:
        """Check that array has at least two elements."""
        min_num = 2
        if self.num < min_num:
            msg = self._err_fmt(
                f"At least {min_num} elements are required for the array, but current size is {self.num}. "
                "Consider using non-array kind instead."
            )
            raise ValueError(msg)
        return self

    @model_validator(mode="after")
    def _check_indices_unique(self) -> Self:
        """Check that all indices are unique."""
        if len(set(self.indices)) != len(self.indices):
            msg = self._err_fmt(f"Indices are not unique: {self.indices}")
            raise ValueError(msg)
        return self

    @model_validator(mode="after")
    def _check_indices_length(self) -> Self:
        """Check that number of indices is greater or equal to number of elements."""
        if len(self.indices) < self.num:
            msg = self._err_fmt(f"Number of indices {len(self.indices)} is less than number of elements {self.num}")
            raise ValueError(msg)
        return self

    @model_validator(mode="after")
    def _check_naming(self) -> Self:
        """Check that naming pattern is valid."""
        try:
            self.naming.format_map(defaultdict(str, index="0"))
        except KeyError as e:
            if str(e) == "'index'":
                msg = self._err_fmt(f"Naming pattern {self.naming} is invalid: missing 'index'")
            else:
                msg = self._err_fmt(f"Naming pattern {self.naming} is invalid")
            raise ValueError(msg) from e
        return self

    @model_validator(mode="after")
    def _update_backlinks(self) -> Self:
        """Update references to parent in all child items."""
        for item in self.generated_items:
            item._assign_parent(self)  # noqa: SLF001
        return self


class EnumMember(Item):
    """Member of a bit field enumeration."""

    value: NonNegativeInt
    """Enumeration value."""

    @property
    def width(self) -> NonNegativeInt:
        """Minimum number of bits required to represent the value."""
        if not hasattr(self, "_width"):
            self._width = self.value.bit_length()
            if self._width == 0:
                self._width = 1  # bit_length() returns zero for zero value, so assign minimum value
        return self._width

    @property
    def parent_enum(self) -> Enum:
        """Parent enumeration."""
        if isinstance(self.parent, Enum):
            return self.parent
        msg = self._err_fmt("Parent is not an instance of `Enum`")
        raise TypeError(msg)

    @model_validator(mode="after")
    def _update_backlinks(self) -> Self:
        """Update references to parent in all child items."""
        # has no children, nothing to update
        return self


class Enum(Item):
    """Enumeration of a bit field."""

    members: tuple[EnumMember, ...]
    """Enumeration members.

    There should be at least one member.
    Members are sorted by value in ascending order.
    """

    @property
    def width(self) -> NonNegativeInt:
        """Minimum number of bits required to represent the largest member of enumeration."""
        if not hasattr(self, "_width"):
            self._width = max(m.width for m in self.members)
        return self._width

    @property
    def names(self) -> Iterator[IdentifierStr]:
        """Iterate over names of members."""
        return (m.name for m in self.members)

    @property
    def values(self) -> Iterator[NonNegativeInt]:
        """Iterate over values of members."""
        return (m.value for m in self.members)

    @property
    def parent_field(self) -> Field:
        """Parent field."""
        if isinstance(self.parent, Field):
            return self.parent
        msg = self._err_fmt("Parent is not an instance of `Field`")
        raise TypeError(msg)

    @field_validator("members", mode="after")
    @classmethod
    def _sort_members(cls, values: tuple[EnumMember, ...]) -> tuple[EnumMember, ...]:
        """Sort members by value."""
        return tuple(sorted(values, key=lambda v: v.value))

    @model_validator(mode="after")
    def _check_members_provided(self) -> Self:
        """Check that at least one member is provided."""
        if len(self.members) == 0:
            msg = self._err_fmt("Empty enumeration is not allowed, at least one member has to be provided")
            raise ValueError(msg)
        return self

    @model_validator(mode="after")
    def _check_members_unique_values(self) -> Self:
        """Check that all values inside enumeration are unique."""
        if len({member.value for member in self.members}) != len(self.members):
            msg = self._err_fmt(f"Some enumeration member values are not unique: {self.members}")
            raise ValueError(msg)
        return self

    @model_validator(mode="after")
    def _check_members_unique_names(self) -> Self:
        """Check that all names inside enumeration are unique."""
        if len({member.name for member in self.members}) != len(self.members):
            msg = self._err_fmt(f"Some enumeration member names are not unique: {self.members}")
            raise ValueError(msg)
        return self

    @model_validator(mode="after")
    def _update_backlinks(self) -> Self:
        """Update references to parent in all child items."""
        for m in self.members:
            m._assign_parent(self)  # noqa: SLF001
        return self


class Field(Item):
    """Bit field inside a register."""

    reset: NonNegativeInt | None
    """Reset value. Can be unknown."""

    offset: NonNegativeInt
    """Bit offset within register."""

    width: PositiveInt
    """Bit width of the item."""

    access: AccessMode
    """Access mode."""

    hardware: HardwareMode
    """Hardware interaction options."""

    enum: Enum | None
    """Optional enumeration for the field."""

    # TODO: volatile if updated by hardware

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

    @property
    def parent_register(self) -> Register:
        """Parent register."""
        if isinstance(self.parent, Register):
            return self.parent
        msg = self._err_fmt("Parent is not a register")
        raise TypeError(msg)

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
            msg = self._err_fmt(f"Provided {byte_idx=} has to be one of {byte_indices} for the field.")
            raise ValueError(msg)

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
        for flag in (HardwareMode.NA, HardwareMode.QUEUE, HardwareMode.FIXED):
            if flag in self.hardware and len(self.hardware) > 1:
                msg = self._err_fmt(f"Hardware mode '{flag}' must be exclusive, but current mode is '{self.hardware}'")
                raise ValueError(msg)

        # Hardware queue mode can be only combined with specific access values
        if HardwareMode.QUEUE in self.hardware:
            q_access_allowed = [AccessMode.RW, AccessMode.RO, AccessMode.WO]
            if self.access not in q_access_allowed:
                msg = self._err_fmt(
                    f"Hardware mode 'q' is allowed to use only with '{q_access_allowed}', "
                    f"but current access mode is '{self.access}'"
                )
                raise ValueError(msg)

        # Enable must be used with Input
        if HardwareMode.ENABLE in self.hardware and HardwareMode.INPUT not in self.hardware:
            msg = self._err_fmt(
                f"Hardware mode 'e' is allowed to use only with 'i', " f"but current hardware mode is '{self.hardware}'"
            )
            raise ValueError(msg)
        return self

    @model_validator(mode="after")
    def _check_reset_width(self) -> Self:
        """Check that reset value width less or equal field width."""
        if self.reset:
            reset_value_width = self.reset.bit_length()
            if reset_value_width > self.width:
                msg = self._err_fmt(
                    f"Reset value 0x{self.reset:x} requires {reset_value_width} bits to represent,"
                    f" but field is {self.width} bits wide"
                )
                raise ValueError(msg)
        return self

    @model_validator(mode="after")
    def _check_enum_members_width(self) -> Self:
        """Check that enumeration members has values, which width fit field width."""
        if self.enum and self.enum.width > self.width:
            msg = self._err_fmt(
                f"Enumeration {self.enum} requires {self.enum.width} bits to represent,"
                f" but field is {self.width} bits wide"
            )
            raise ValueError(msg)
        return self

    @model_validator(mode="after")
    def _update_backlinks(self) -> Self:
        """Update references to parent in all child items."""
        if self.enum:
            self.enum._assign_parent(self)  # noqa: SLF001
        return self


class Register(MapableItem):
    """Control and Status Register."""

    fields: tuple[Field, ...]
    """Bit fields inside a register.

    Fields are sorted from LSB to MSB.
    """

    @property
    def width(self) -> PositiveInt:
        """Register bit width."""
        # TODO: get width from parent map
        raise NotImplementedError

    @property
    def access(self) -> AccessCategory:
        """Access rights based on access modes of the fields."""
        if not hasattr(self, "_access"):
            if all(f.access.is_ro for f in self.fields):
                self._access = AccessCategory.RO
            elif all(f.access.is_wo for f in self.fields):
                self._access = AccessCategory.WO
            else:
                self._access = AccessCategory.RW
        return self._access

    @property
    def reset(self) -> NonNegativeInt:
        """Reset value based on reset values of the fields.

        Unknown reset value for a field converted to zero.
        """
        if not hasattr(self, "_reset"):
            self._reset = 0
            for f in self.fields:
                self._reset |= (f.reset if f.reset else 0) << f.lsb
        return self._reset

    @property
    def reset_binstr(self) -> str:
        """Reset value represented as a binary string where unknown bits masked as 'x'.

        No any prefix. Leading zeroes are added to match `width`.
        Examples: 00110, 1x10
        """
        if not hasattr(self, "_reset_binstr"):
            bits = ["0"] * self.width
            for f in self.fields:
                if f.reset:
                    bits[f.lsb : f.msb + 1] = list(f"{f.reset:0{f.width}b}")
                else:
                    bits[f.lsb : f.msb + 1] = ["x"] * f.width
            self._reset_binstr = "".join(reversed(bits))
        return self._reset_binstr

    @property
    def reset_hexstr(self) -> str:
        """Reset value represented as a hexadecimal string where unknown nibbles masked as 'x'.

        No any prefix. Leading zeroes are added to match `width`.
        Examples: 0002bca, x2ax
        """
        if not hasattr(self, "_reset_hexstr"):
            nibbles = ["0"] * (self.width // 4)
            for i in range(len(nibbles)):
                bit_slice = self.reset_binstr[i * 4 : i * 4 + 4]
                if "x" in bit_slice:
                    nibbles[i] = "x"
                else:
                    nibbles[i] = f"{int(bit_slice):x}"
            self._reset_hexstr = "".join(reversed(nibbles))
        return self._reset_hexstr

    @field_validator("fields", mode="after")
    @classmethod
    def _sort_fields(cls, values: tuple[Field, ...]) -> tuple[Field, ...]:
        """Sort fields by LSB."""
        return tuple(sorted(values, key=lambda v: v.lsb))

    @model_validator(mode="after")
    def _check_fields_unique_names(self) -> Self:
        """Check that all field names inside register are unique."""
        names = [field.name for field in self.fields]
        duplicates = {name for name in names if names.count(name) > 1}
        if duplicates:
            msg = self._err_fmt(f"Some field names are not unique and used more than once: {duplicates}")
            raise ValueError(msg)
        return self

    @model_validator(mode="after")
    def _check_fields_overlapping(self) -> Self:
        """Check that no fields overlap other ones."""
        field_bits = {field.name: set(field.bit_indices) for field in self.fields}

        for field in self.fields:
            overlaps = {
                name: bool(set(field.bit_indices).intersection(bits))
                for name, bits in field_bits.items()
                if name != field.name
            }
            if any(v for v in overlaps.values()):
                msg = self._err_fmt(f"Field {field.name} overlaps with other fields: {', '.join(overlaps.keys())}")
                raise ValueError(msg)
        return self

    @model_validator(mode="after")
    def _check_fields_width(self) -> Self:
        """Check that all fields fit register width."""
        last_field = self.fields[-1]
        if last_field.msb >= self.width:
            msg = self._err_fmt(
                f"Field {last_field.name} (lsb={last_field.lsb} msb={last_field.msb}) "
                f"exceeds size {self.width} of the register"
            )
            raise ValueError(msg)
        return self

    @model_validator(mode="after")
    def _update_refs(self) -> Self:
        """Update references to parent in all child items."""
        for field in self.fields:
            field._assign_parent(self)  # noqa: SLF001
        return self


class Memory(MapableItem):
    """Memory block."""

    address_width: PositiveInt
    """Memory address bit width."""

    data_width: PositiveInt
    """Memory data bit width."""

    style: MemoryStyle
    """Memory implementation style."""

    initial_values: tuple[tuple[NonNegativeInt, NonNegativeInt], ...]
    """Initial values for selected memory locations.

    Each tuple contains address and value.
    """

    @property
    def size(self) -> Pow2Int:
        """Memory size in bytes."""
        return 2**self.address_width

    @property
    def granularity(self) -> Pow2Int:
        """Memory granularity in bytes."""
        return math.ceil(self.data_width / 8)

    @property
    def access(self) -> AccessCategory:
        """Memory access rights for CSR map."""
        return self.style.access


class Map(MapableItem):
    """Collection of memory-mapped items."""

    size: Pow2Int
    """Byte size of address space that map covers."""

    granularity: Pow2Int
    """Byte size of a single register within map."""

    items: tuple[MapableItem, ...]
    """Items within the map. Should be not empty.

    Items are sorted by offsets.
    """

    @property
    def maps(self) -> Iterator[Map]:
        """Iterate through all submaps within map. Iterator might be empty."""
        return (item for item in self.items if isinstance(item, Map))

    @property
    def registers(self) -> Iterator[Register]:
        """Iterate through all registers within map. Iterator might be empty."""
        return (item for item in self.items if isinstance(item, Register))

    @property
    def memories(self) -> Iterator[Memory]:
        """Iterate through all memories within map. Iterator might be empty."""
        return (item for item in self.items if isinstance(item, Memory))

    @property
    def address_width(self) -> PositiveInt:
        """Address bit width."""
        return int(math.log2(self.size))

    @property
    def register_width(self) -> PositiveInt:
        """Register data bit width."""
        return self.granularity * 8

    @property
    def is_root(self) -> bool:
        """Check if current map is a root map."""
        return not hasattr(self, "_parent")

    @property
    def has_maps(self) -> bool:
        """Check if current map contains submaps."""
        return any(isinstance(item, Map) for item in self.items)

    @property
    def has_registers(self) -> bool:
        """Check if current map contains registers."""
        return any(isinstance(item, Register) for item in self.items)

    @property
    def has_memories(self) -> bool:
        """Check if current map contains memory blocks."""
        return any(isinstance(item, Memory) for item in self.items)

    @property
    def address(self) -> NonNegativeInt:
        """Global byte address of the item."""
        # root map has no parent, so its address is its offset
        return self.offset if self.is_root else super().address

    @field_validator("items", mode="after")
    @classmethod
    def _sort_items(cls, values: tuple[MapableItem, ...]) -> tuple[MapableItem, ...]:
        """Sort items by offset."""
        return tuple(sorted(values, key=lambda v: v.offset))

    @model_validator(mode="after")
    def _check_items_unique_names(self) -> Self:
        """Check that all item names inside map are unique."""
        names = [item.name for item in self.items]
        duplicates = {name for name in names if names.count(name) > 1}
        if duplicates:
            msg = self._err_fmt(f"Some item names are not unique and used more than once: {duplicates}")
            raise ValueError(msg)
        return self

    @model_validator(mode="after")
    def _check_items_unique_offsets(self) -> Self:
        """Check that all item offsets inside map are unique."""
        offsets = [item.offset for item in self.items]
        duplicates = {offset for offset in offsets if offsets.count(offset) > 1}
        if duplicates:
            msg = self._err_fmt(f"Some item offsets are not unique and used more than once: {duplicates}")
            raise ValueError(msg)
        return self

    # TODO: check that all offsets are aligned to map granularity
    # TODO: check that there is no address collisions between items
    # TODO: check that all maps/memories within map has proper `address_width` (less or equal to map address width)
    # TODO: check that all array items within map has correct `increment`
    # TODO: check that no register is falling out of the root map address space

    @model_validator(mode="after")
    def _update_refs(self) -> Self:
        """Update references to parent in all child items."""
        for item in self.items:
            item._assign_parent(self)  # noqa: SLF001
        return self


class FieldArray(Field, ArrayItem):
    """Logical collection of similar fields with common properties."""

    @property
    def generated_fields(self) -> tuple[Field, ...]:
        """Generated fields in the array."""
        # _generate_items creates tuple of `Field` items, so waiver is safe here
        return self.generated_items  # type: ignore reportReturnType

    def _generate_items(self) -> tuple[Item, ...]:
        """Generate concrete fields in the array."""
        raise NotImplementedError


class RegisterArray(Register, ArrayItem):
    """Logical collection of similar registers with common properties."""

    @property
    def generated_registers(self) -> tuple[Register, ...]:
        """Concrete registers in the array."""
        # _generate_items creates tuple of `Register` items, so waiver is safe here
        return self.generated_items  # type: ignore reportReturnType

    def _generate_items(self) -> tuple[Item, ...]:
        """Generate concrete items in the array."""
        raise NotImplementedError


class MemoryArray(Memory, ArrayItem):
    """Logical collection of similar memory blocks with common properties."""

    @property
    def generated_memories(self) -> tuple[Memory, ...]:
        """Generated memories in the array."""
        # _generate_items creates tuple of `Memory` items, so waiver is safe here
        return self.generated_items  # type: ignore reportReturnType

    def _generate_items(self) -> tuple[Item, ...]:
        """Generate concrete items in the array."""
        raise NotImplementedError


class MapArray(Map, ArrayItem):
    """Logical collection of similar maps with common properties."""

    @property
    def generated_maps(self) -> tuple[Map, ...]:
        """Generated maps in the array."""
        # _generate_items creates tuple of `Map` items, so waiver is safe here
        return self.generated_items  # type: ignore reportReturnType

    def _generate_items(self) -> tuple[Item, ...]:
        """Generate concrete items in the array."""
        raise NotImplementedError
