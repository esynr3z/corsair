"""Enumeration for hardare modes of a bitfield."""

from __future__ import annotations

from enum import Flag
from typing import TYPE_CHECKING, Iterable, Iterator

if TYPE_CHECKING:
    from enum import Enum

    from typing_extensions import Self


class HwMode(str, Flag):
    """Hardware mode for a bitfield.

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
    def _missing_(cls, value: object) -> Enum:
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
        # Code below allows "ioe" and "i|o|e" as well.
        raw_flags = set(value.split("|") if "|" in value else value)

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
        return "|".join(flags)

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
