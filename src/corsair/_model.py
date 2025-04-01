"""Internal register model."""

from __future__ import annotations

import enum
import functools
import itertools
import math
from abc import ABC, abstractmethod
from collections import defaultdict
from typing import TYPE_CHECKING, Annotated, Any, Literal

from pydantic import (
    BaseModel,
    ConfigDict,
    Discriminator,
    Tag,
    ValidationInfo,
    field_validator,
    model_validator,
)
from pydantic.types import NonNegativeInt, PositiveInt

from ._types import IdentifierStr, Pow2Int, SingleLineStr, TextStr

if TYPE_CHECKING:
    from collections.abc import Iterable, Iterator

    from typing_extensions import Self


class FrozenProperty(functools.cached_property):
    """Read-only cached property that calculates value on first access and forbids any changes."""

    def __set__(self, instance: object, value: Any) -> None:
        raise AttributeError(f"Cannot set value of read-only property {self.func.__name__}")

    def __delete__(self, instance: object) -> None:
        raise AttributeError(f"Cannot delete value of read-only property {self.func.__name__}")


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


class ItemMetadata(BaseModel):
    """Metadata for an item."""

    # All fields are created by user

    model_config = ConfigDict(
        # Model is faux-immutable
        frozen=True,
        # Extra values are allowed
        extra="allow",
    )


class NamedItem(BaseModel, ABC):
    """Base data structure for all CSR model internal items: map, register, field, etc.

    Its immutability allows to provide solid contract for generators, when they traverse the model.
    Immutability also allows to cache properties to avoid recalculations and use model hashing.

    This class provides basic functionality to differentiate an item from other items
    and understand its place in the hierarchy.
    """

    model_config = ConfigDict(
        # Docstrings of attributesshould be used for field descriptions
        use_attribute_docstrings=True,
        # Model is faux-immutable
        frozen=True,
        # Extra values are not permitted
        extra="forbid",
        # Hide input in errors
        hide_input_in_errors=True,
        # Types below are not fields, but properties
        ignored_types=(FrozenProperty,),
    )

    name: IdentifierStr
    """Name of an item."""

    doc: TextStr
    """Docstring for an item.

    Follows Python docstring rules - first line is a brief summary,
    then optionally, empty line following detailed multiline description.
    """

    metadata: ItemMetadata = ItemMetadata()
    """Optional user metadata attached to an item."""

    # Private fields to store property values
    _parent: NamedItem | None = None

    @FrozenProperty
    def brief(self) -> SingleLineStr:
        """Brief description for an item, derived from `doc`.

        First line of `doc` is used.
        """
        return self.doc.split("\n", 1)[0].strip()

    @FrozenProperty
    def description(self) -> TextStr:
        """Detailed description for an item, derived from `doc`.

        For a single-line `doc` it is the same as `brief`, but for multiline text block following brief is returned.
        """
        parts = self.doc.split("\n", 1)
        return (parts[1] if len(parts) > 1 else parts[0]).strip()

    @FrozenProperty
    def path(self) -> str:
        """Full path in object hierarchy."""
        return self.name if self.parent is None else f"{self.parent.path}.{self.name}"

    @property
    def parent(self) -> NamedItem | None:
        """Parent for the current register model item."""
        return self._parent

    @property
    @abstractmethod
    def _children(self) -> tuple[NamedItem, ...]:
        """All subitems within item."""

    @model_validator(mode="after")
    def _update_backlinks(self) -> Self:
        """Update backlinks to current parent in all child items and clear relevant caches."""
        for child in self._children:
            # Set the parent first
            child._parent = self  # noqa: SLF001

            # Clear all FrozenProperty caches on the child
            # This ensures that properties recalculated after the parent is set.
            for attr_name, attr_value in type(child).__dict__.items():
                if isinstance(attr_value, FrozenProperty):
                    # The cached value is stored in the instance's dict with the property name.
                    # Use pop with a default to avoid KeyError if the cache wasn't populated yet.
                    child.__dict__.pop(attr_name, None)

        return self


class MapableItem(NamedItem):
    """NamedItem that can be mappend into global address space.

    This class add properties to work with address space and get address of the item.
    """

    offset: NonNegativeInt
    """Byte offset from the parent addressable item."""

    @FrozenProperty
    def base_address(self) -> NonNegativeInt:
        """Address, which this item is offsetted from."""
        if self.parent is None:
            return 0
        if not isinstance(self.parent, MapableItem):
            raise TypeError("Parent has to be a `MapableItem`")
        return self.parent.address

    @FrozenProperty
    def address(self) -> NonNegativeInt:
        """Global address of the item."""
        return self.base_address + self.offset


class ArrayItem(NamedItem):
    """`NamedItem` that can describe array of items with common properties following some repeatable pattern."""

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

    @FrozenProperty
    def generated_items(self) -> tuple[NamedItem, ...]:
        """Concrete items in array created by following the pattern."""
        return self._generate_items()

    @abstractmethod
    def _generate_items(self) -> tuple[NamedItem, ...]:
        """Generate concrete items in the array."""

    @field_validator("indices", mode="after")
    @classmethod
    def _fill_indices(cls, values: tuple[str, ...], info: ValidationInfo) -> tuple[str, ...]:
        """Fill indices with numeric values if they are not provided."""
        if not values:
            return tuple(str(i) for i in range(info.data["num"]))
        return values

    @model_validator(mode="after")
    def _validate_minimum_num(self) -> Self:
        """Validate that array has at least two elements."""
        min_num = 2
        if self.num < min_num:
            raise ValueError(
                f"At least {min_num} elements are required for the array, but current size is {self.num}. "
                "Consider using non-array kind instead."
            )
        return self

    @model_validator(mode="after")
    def _validate_indices_unique(self) -> Self:
        """Validate that all indices are unique."""
        if len(set(self.indices)) != len(self.indices):
            raise ValueError(f"Indices are not unique: {self.indices}")
        return self

    @model_validator(mode="after")
    def _validate_indices_length(self) -> Self:
        """Validate that number of indices is greater or equal to number of elements."""
        if len(self.indices) < self.num:
            raise ValueError(
                f"Number of indices {len(self.indices)} is less than number of elements {self.num}. "
                "Consider using non-array kind instead."
            )
        return self

    @model_validator(mode="after")
    def _validate_naming(self) -> Self:
        """Validate that naming pattern is valid."""
        try:
            self.naming.format_map(defaultdict(str, index="0"))
        except KeyError as e:
            if str(e) == "'index'":
                raise ValueError(f"Naming pattern {self.naming} is invalid: missing 'index'") from e
            raise ValueError(f"Naming pattern {self.naming} is invalid") from e
        return self


class EnumMember(NamedItem):
    """Member of a bit field enumeration."""

    value: NonNegativeInt
    """Enumeration value."""

    @FrozenProperty
    def width(self) -> NonNegativeInt:
        """Minimum number of bits required to represent the value."""
        return max(self.value.bit_length(), 1)

    @property
    def parent_enum(self) -> Enum:
        """Parent enumeration.

        Requires parent to be set.
        """
        if self.parent is None:
            raise ValueError("Parent has to be set before accessing parent enum")
        if not isinstance(self.parent, Enum):
            raise TypeError("Parent is not an instance of `Enum`")
        return self.parent

    @property
    def _children(self) -> tuple[NamedItem, ...]:
        """All subitems within item."""
        return ()


class Enum(NamedItem):
    """Enumeration of a bit field."""

    members: tuple[EnumMember, ...]
    """Enumeration members.

    There should be at least one member.
    Members are sorted by value in ascending order.
    """

    @FrozenProperty
    def width(self) -> NonNegativeInt:
        """Minimum number of bits required to represent the largest member of enumeration."""
        return max(m.width for m in self.members)

    @FrozenProperty
    def names(self) -> tuple[IdentifierStr, ...]:
        """Names of members."""
        return tuple(m.name for m in self.members)

    @FrozenProperty
    def values(self) -> tuple[NonNegativeInt, ...]:
        """Values of members."""
        return tuple(m.value for m in self.members)

    @property
    def parent_field(self) -> Field:
        """Parent field.

        Requires parent to be set.
        """
        if self.parent is None:
            raise ValueError("Parent has to be set before accessing parent field")
        if not isinstance(self.parent, Field):
            raise TypeError("Parent is not an instance of `Field`")
        return self.parent

    @property
    def _children(self) -> tuple[NamedItem, ...]:
        """All subitems within item."""
        return self.members

    @field_validator("members", mode="after")
    @classmethod
    def _sort_members(cls, values: tuple[EnumMember, ...]) -> tuple[EnumMember, ...]:
        """Sort members by value."""
        return tuple(sorted(values, key=lambda v: v.value))

    @field_validator("members", mode="after")
    @classmethod
    def _validate_members_provided(cls, values: tuple[EnumMember, ...]) -> tuple[EnumMember, ...]:
        """Validate that at least one member is provided."""
        if len(values) == 0:
            raise ValueError("Empty enumeration is not allowed, at least one member has to be provided")
        return values

    @field_validator("members", mode="after")
    @classmethod
    def _validate_members_unique_values(cls, values: tuple[EnumMember, ...]) -> tuple[EnumMember, ...]:
        """Validate that all values inside enumeration are unique."""
        if len({member.value for member in values}) != len(values):
            raise ValueError("Some enumeration member values are not unique")
        return values

    @field_validator("members", mode="after")
    @classmethod
    def _validate_members_unique_names(cls, values: tuple[EnumMember, ...]) -> tuple[EnumMember, ...]:
        """Validate that all names inside enumeration are unique."""
        if len({member.name for member in values}) != len(values):
            raise ValueError("Some enumeration member names are not unique")
        return values


class Field(NamedItem):
    """Bit field inside a register."""

    offset: NonNegativeInt
    """Bit offset within register."""

    width: PositiveInt
    """Bit width of the item."""

    reset: NonNegativeInt | None
    """Reset value. Can be unknown."""

    access: AccessMode
    """Access mode."""

    hardware: HardwareMode
    """Hardware interaction options."""

    enum: Enum | None
    """Optional enumeration for the field."""

    @FrozenProperty
    def bit_indices(self) -> tuple[int, ...]:
        """Field bit positions inside register from LSB to MSB."""
        return tuple(range(self.offset, self.offset + self.width))

    @FrozenProperty
    def byte_indices(self) -> tuple[int, ...]:
        """Field byte indices inside register from lower to higher."""
        return tuple(range(self.offset // 8, (self.offset + self.width - 1) // 8 + 1))

    @FrozenProperty
    def lsb(self) -> int:
        """Position of the least significant bit (LSB) inside register."""
        return self.offset

    @FrozenProperty
    def msb(self) -> int:
        """Position of the most significant bit (MSB) inside register."""
        return self.lsb + self.width - 1

    @FrozenProperty
    def mask(self) -> int:
        """Bit mask for the bitfield inside register."""
        return (2 ** (self.width) - 1) << self.offset

    @FrozenProperty
    def is_multibit(self) -> bool:
        """Bitfield has more than one bit width."""
        return self.width > 1

    @FrozenProperty
    def parent_register(self) -> Register:
        """Parent register.

        Requires parent to be set.
        """
        if self.parent is None:
            raise ValueError("Parent has to be set before accessing parent register")
        if not isinstance(self.parent, Register):
            raise TypeError("Parent is not an instance of `Register`")
        return self.parent

    @property
    def _children(self) -> tuple[NamedItem, ...]:
        """All subitems within item."""
        return (self.enum,) if self.enum else ()

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

    @field_validator("hardware", mode="after")
    @classmethod
    def _validate_hardware_constraints(cls, value: HardwareMode, info: ValidationInfo) -> HardwareMode:
        """Validate that `hardware` field follows expected constraints."""
        # Check exclusive hardware flags
        for flag in (HardwareMode.NA, HardwareMode.QUEUE, HardwareMode.FIXED):
            if flag in value and len(value) > 1:
                raise ValueError(f"Hardware mode '{flag}' must be exclusive, but current mode is '{value}'")

        # Hardware queue mode can be only combined with specific access values
        if HardwareMode.QUEUE in value:
            q_access_allowed = [AccessMode.RW, AccessMode.RO, AccessMode.WO]
            if info.data["access"] not in q_access_allowed:
                raise ValueError(
                    f"Hardware mode 'q' is allowed to use only with '{q_access_allowed}', "
                    f"but current access mode is '{info.data['access']}'"
                )

        # Enable must be used with Input
        if HardwareMode.ENABLE in value and HardwareMode.INPUT not in value:
            raise ValueError(
                f"Hardware mode 'e' is allowed to use only with 'i', " f"but current hardware mode is '{value}'"
            )
        return value

    @field_validator("reset", mode="after")
    @classmethod
    def _validate_reset_width(cls, value: NonNegativeInt | None, info: ValidationInfo) -> NonNegativeInt | None:
        """Validate that reset value width less or equal field width."""
        if value is not None:
            reset_value_width = value.bit_length()
            if reset_value_width > info.data["width"]:
                raise ValueError(
                    f"Reset value 0x{value:x} requires {reset_value_width} bits to represent,"
                    f" but field is {info.data['width']} bits wide"
                )
        return value

    @field_validator("enum", mode="after")
    @classmethod
    def _validate_enum_members_width(cls, value: Enum | None, info: ValidationInfo) -> Enum | None:
        """Validate that enumeration members has values, which width fit field width."""
        if value is not None and value.width > info.data["width"]:
            raise ValueError(
                f"Enumeration {value} requires {value.width} bits to represent,"
                f" but field is {info.data['width']} bits wide"
            )
        return value


class Register(MapableItem):
    """Control and Status Register."""

    kind: Literal["register"] = "register"
    """Item kind discriminator."""

    fields: tuple[Field, ...]
    """Bit fields inside a register.

    Fields are sorted from LSB to MSB.
    """

    @property
    def parent_map(self) -> Map:
        """Parent map.

        Requires parent to be set.
        """
        if self.parent is None:
            raise ValueError("Parent has to be set before accessing parent map")
        if not isinstance(self.parent, Map):
            raise TypeError("Parent is not an instance of `Map`")
        return self.parent

    @property
    def _children(self) -> tuple[NamedItem, ...]:
        """All subitems within item."""
        return self.fields

    @FrozenProperty
    def width(self) -> NonNegativeInt:
        """Minimum number of bits required to represent the register."""
        return max(f.msb for f in self.fields) + 1

    @FrozenProperty
    def access(self) -> AccessCategory:
        """Access rights based on access modes of the fields."""
        if all(f.access.is_ro for f in self.fields):
            return AccessCategory.RO
        if all(f.access.is_wo for f in self.fields):
            return AccessCategory.WO
        return AccessCategory.RW

    @FrozenProperty
    def reset(self) -> NonNegativeInt:
        """Reset value based on reset values of the fields.

        Unknown reset value for a field converted to zero.
        """
        return sum(f.reset << f.lsb for f in self.fields if f.reset is not None)

    @FrozenProperty
    def reset_binstr(self) -> str:
        """Reset value represented as a binary string where unknown bits masked as 'x'.

        No any prefix. Leading zeroes are added to match `width`.
        Examples: 00110, 1x10
        """
        bits = ["0"] * self.width
        for f in self.fields:
            if f.reset:
                bits[f.lsb : f.msb + 1] = list(f"{f.reset:0{f.width}b}")
            else:
                bits[f.lsb : f.msb + 1] = ["x"] * f.width
        return "".join(reversed(bits))

    @FrozenProperty
    def reset_hexstr(self) -> str:
        """Reset value represented as a hexadecimal string where unknown nibbles masked as 'x'.

        No any prefix. Leading zeroes are added to match `width`.
        Examples: 0002bca, x2ax
        """
        nibbles = ["0"] * math.ceil(self.width / 4)
        for i in range(len(nibbles)):
            bit_slice = self.reset_binstr[::-1][i * 4 : i * 4 + 4]
            if "x" in bit_slice:
                nibbles[i] = "x"
            else:
                nibbles[i] = f"{int(bit_slice, 2):x}"
        return "".join(nibbles)

    @field_validator("fields", mode="after")
    @classmethod
    def _sort_fields(cls, values: tuple[Field, ...]) -> tuple[Field, ...]:
        """Sort fields by LSB."""
        return tuple(sorted(values, key=lambda v: v.lsb))

    @model_validator(mode="after")
    def _validate_fields_unique_names(self) -> Self:
        """Validate that all field names inside register are unique."""
        names = [field.name for field in self.fields]
        duplicates = {name for name in names if names.count(name) > 1}
        if duplicates:
            raise ValueError(f"Some field names are not unique and used more than once: {duplicates}")
        return self

    @model_validator(mode="after")
    def _validate_fields_overlapping(self) -> Self:
        """Validate that no fields overlap other ones."""
        field_bits = {field.name: set(field.bit_indices) for field in self.fields}

        for field in self.fields:
            overlaps = {
                name: bool(set(field.bit_indices).intersection(bits))
                for name, bits in field_bits.items()
                if name != field.name
            }
            if any(v for v in overlaps.values()):
                raise ValueError(f"Field {field.name} overlaps with other fields: {', '.join(overlaps.keys())}")
        return self


class Memory(MapableItem):
    """Memory block."""

    kind: Literal["memory"] = "memory"
    """Item kind discriminator."""

    address_width: PositiveInt
    """Memory address bit width."""

    data_width: PositiveInt
    """Memory data bit width."""

    style: MemoryStyle
    """Memory implementation style."""

    initial_values: tuple[tuple[NonNegativeInt, NonNegativeInt], ...]
    """Initial values for selected memory locations.

    Each tuple contains memory word index (address within memory) and value.
    """

    @FrozenProperty
    def capacity(self) -> Pow2Int:
        """Memory capacity in memory words."""
        return 2**self.address_width

    @FrozenProperty
    def size(self) -> Pow2Int:
        """Memory size in bytes."""
        return self.capacity * self.granularity

    @FrozenProperty
    def granularity(self) -> PositiveInt:
        """Memory granularity in bytes."""
        return math.ceil(self.data_width / 8)

    @FrozenProperty
    def access(self) -> AccessCategory:
        """Memory access rights for CSR map."""
        return self.style.access

    @property
    def parent_map(self) -> Map:
        """Parent map.

        Requires parent to be set.
        """
        if self.parent is None:
            raise ValueError("Parent has to be set before accessing parent map")
        if not isinstance(self.parent, Map):
            raise TypeError("Parent is not an instance of `Map`")
        return self.parent

    @property
    def _children(self) -> tuple[NamedItem, ...]:
        """All subitems within item."""
        return ()

    @model_validator(mode="after")
    def _validate_initial_values(self) -> Self:
        """Validate that initial values are valid."""
        for i, (addr, value) in enumerate(self.initial_values):
            if addr >= self.capacity:
                raise ValueError(f"Initial value {i} address 0x{addr:x} is out of memory capacity 0x{self.capacity:x}")
            if value >= 2**self.data_width:
                raise ValueError(
                    f"Initial value {i} data 0x{value:x} is out of memory data width {self.data_width} bits"
                )
        return self


def _get_discriminator_for_mapable_item(v: MapableItem | dict) -> str:
    """Get discriminator value for mapable item.

    When discriminator is not present in the item,
    it is assumed to be a register.
    """
    if isinstance(v, dict):
        return v.get("kind", "register")
    return getattr(v, "kind", "register")


AnyMapableItem = Annotated[
    Annotated["Map", Tag("map")] | Annotated[Register, Tag("register")] | Annotated[Memory, Tag("memory")],
    Discriminator(_get_discriminator_for_mapable_item),
]
"""Union of all known mapable items."""


class Map(MapableItem):
    """Collection of memory-mapped items."""

    kind: Literal["map"] = "map"
    """Item kind discriminator."""

    address_width: PositiveInt
    """Map address bit width."""

    register_width: Pow2Int
    """Map register bit width."""

    items: tuple[AnyMapableItem, ...]
    """Items within the map. Should be not empty.

    Items are sorted by offsets.
    """

    @FrozenProperty
    def size(self) -> Pow2Int:
        """Byte size of address space that map covers."""
        return 2**self.address_width

    @FrozenProperty
    def granularity(self) -> Pow2Int:
        """Byte size of a single register within map."""
        return math.ceil(self.register_width / 8)

    @FrozenProperty
    def maps(self) -> tuple[Map, ...]:
        """All submaps within map."""
        return tuple(item for item in self.items if isinstance(item, Map))

    @FrozenProperty
    def registers(self) -> tuple[Register, ...]:
        """All registers within map."""
        return tuple(item for item in self.items if isinstance(item, Register))

    @FrozenProperty
    def memories(self) -> tuple[Memory, ...]:
        """All memories within map."""
        return tuple(item for item in self.items if isinstance(item, Memory))

    @FrozenProperty
    def has_maps(self) -> bool:
        """Check if current map contains submaps."""
        return any(self.maps)

    @FrozenProperty
    def has_registers(self) -> bool:
        """Check if current map contains registers."""
        return any(self.registers)

    @FrozenProperty
    def has_memories(self) -> bool:
        """Check if current map contains memory blocks."""
        return any(self.memories)

    @FrozenProperty
    def address(self) -> NonNegativeInt:
        """Global byte address of the item."""
        # root map has no parent, so its address is its offset
        return self.offset if self.is_root else super().address

    @property
    def is_root(self) -> bool:
        """Check if current map is a root map."""
        return self.parent is None

    @property
    def parent_map(self) -> Map:
        """Parent map.

        Requires parent to be set.
        """
        if self.parent is None:
            raise ValueError("Parent has to be set before accessing parent map")
        if not isinstance(self.parent, Map):
            raise TypeError("Parent is not an instance of `Map`")
        return self.parent

    @property
    def _children(self) -> tuple[NamedItem, ...]:
        """All subitems within item."""
        return self.items

    @field_validator("items", mode="after")
    @classmethod
    def _sort_items(cls, values: tuple[MapableItem, ...]) -> tuple[MapableItem, ...]:
        """Sort items by offset."""
        return tuple(sorted(values, key=lambda v: v.offset))

    @model_validator(mode="after")
    def _validate_items_provided(self) -> Self:
        """Validate that at least one item is provided."""
        if len(self.items) == 0:
            raise ValueError("Empty map is not allowed, at least one item has to be provided")
        return self

    @model_validator(mode="after")
    def _validate_min_register_width(self) -> Self:
        """Validate that register width is at least single byte."""
        min_width = 8
        if self.register_width < min_width:
            raise ValueError(
                f"Minimal allowed 'register_width' for a map is {min_width}, but {self.register_width} provided"
            )
        return self

    @model_validator(mode="after")
    def _validate_items_unique_names(self) -> Self:
        """Validate that all item names inside map are unique."""
        names = [item.name for item in self.items]
        duplicates = {name for name in names if names.count(name) > 1}
        if duplicates:
            raise ValueError(f"Some item names are not unique and used more than once: {duplicates}")
        return self

    @model_validator(mode="after")
    def _validate_items_unique_offsets(self) -> Self:
        """Validate that all item offsets inside map are unique."""
        offsets = [item.offset for item in self.items]
        duplicates = {offset for offset in offsets if offsets.count(offset) > 1}
        if duplicates:
            raise ValueError(f"Some item offsets are not unique and used more than once: {duplicates}")
        return self

    @model_validator(mode="after")
    def _validate_items_offset_alignment(self) -> Self:
        """Validate that all item offsets are aligned to the map granularity."""
        for item in self.items:
            if item.offset % self.granularity != 0:
                raise ValueError(
                    f"Item {item.name} offset 0x{item.offset:x} is not aligned to map granularity {self.granularity}"
                )
        return self

    @model_validator(mode="after")
    def _validate_items_address_width(self) -> Self:
        """Validate that all child maps and memories have address width less or equal to current map address width."""
        for item in itertools.chain(self.maps, self.memories):
            if item.address_width > self.address_width:
                raise ValueError(
                    f"Item {item.name} address width {item.address_width} is "
                    f"greater than map address width {self.address_width}"
                )
        return self

    @model_validator(mode="after")
    def _validate_items_address_collisions(self) -> Self:
        """Validate that there is no address collisions between items."""
        item_address_ranges: dict[AnyMapableItem, tuple[NonNegativeInt, NonNegativeInt]] = {}
        for item in self.items:
            if isinstance(item, Map | Memory):
                item_address_ranges[item] = (item.offset, item.offset + item.size - 1)
            elif isinstance(item, Register):
                item_address_ranges[item] = (
                    item.offset,
                    item.offset + self.granularity - 1,
                )

        # Check for collisions
        for item, (start, end) in item_address_ranges.items():
            for other_item, (other_start, other_end) in item_address_ranges.items():
                if item is other_item:
                    continue
                if start <= other_end and end >= other_start:
                    raise ValueError(f"Address collision between {item.name} and {other_item.name}")

        # Check that no item is falling out of the root map address space
        for item, (start, end) in item_address_ranges.items():
            if end >= self.size:
                raise ValueError(
                    f"Item {item.name} address range [0x{start:x};0x{end+1:x}) is "
                    f"falling out of the root map address space [0x0;0x{self.size:x})"
                )
        return self

    @model_validator(mode="after")
    def _validate_register_fields_width(self) -> Self:
        """Validate that all fields fit register width."""
        for reg in self.registers:
            last_field = reg.fields[-1]
            if last_field.msb >= self.register_width:
                raise ValueError(
                    f"Field {last_field.name} (lsb={last_field.lsb} msb={last_field.msb}) "
                    f"exceeds size {self.register_width} of the register within map"
                )
        return self

    @model_validator(mode="after")
    def _validate_array_items_increment(self) -> Self:
        """Validate that all array items within map has correct `increment`."""
        # TODO: implement
        return self


class FieldArray(Field, ArrayItem):
    """Logical collection of similar fields with common properties."""

    kind: Literal["field_array"] = "field_array"  # type: ignore reportIncompatibleVariableOverride
    """Item kind discriminator."""

    @property
    def generated_fields(self) -> tuple[Field, ...]:
        """Generated fields in the array."""
        # _generate_items creates tuple of `Field` items, so waiver is safe here
        return self.generated_items  # type: ignore reportReturnType

    def _generate_items(self) -> tuple[NamedItem, ...]:
        """Generate concrete fields in the array."""
        raise NotImplementedError


class RegisterArray(Register, ArrayItem):
    """Logical collection of similar registers with common properties."""

    kind: Literal["register_array"] = "register_array"  # type: ignore reportIncompatibleVariableOverride
    """Item kind discriminator."""

    @property
    def generated_registers(self) -> tuple[Register, ...]:
        """Concrete registers in the array."""
        # _generate_items creates tuple of `Register` items, so waiver is safe here
        return self.generated_items  # type: ignore reportReturnType

    def _generate_items(self) -> tuple[NamedItem, ...]:
        """Generate concrete items in the array."""
        raise NotImplementedError


class MemoryArray(Memory, ArrayItem):
    """Logical collection of similar memory blocks with common properties."""

    kind: Literal["memory_array"] = "memory_array"  # type: ignore reportIncompatibleVariableOverride
    """Item kind discriminator."""

    @property
    def generated_memories(self) -> tuple[Memory, ...]:
        """Generated memories in the array."""
        # _generate_items creates tuple of `Memory` items, so waiver is safe here
        return self.generated_items  # type: ignore reportReturnType

    def _generate_items(self) -> tuple[NamedItem, ...]:
        """Generate concrete items in the array."""
        raise NotImplementedError


class MapArray(Map, ArrayItem):
    """Logical collection of similar maps with common properties."""

    kind: Literal["map_array"] = "map_array"  # type: ignore reportIncompatibleVariableOverride
    """Item kind discriminator."""

    @property
    def generated_maps(self) -> tuple[Map, ...]:
        """Generated maps in the array."""
        # _generate_items creates tuple of `Map` items, so waiver is safe here
        return self.generated_items  # type: ignore reportReturnType

    def _generate_items(self) -> tuple[NamedItem, ...]:
        """Generate concrete items in the array."""
        raise NotImplementedError
