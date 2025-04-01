"""Tests for base register map item."""

from __future__ import annotations

from typing import Any

import pytest
from pydantic import ValidationError

import corsair as csr

# All tests below can be used in smoke testing
pytestmark = pytest.mark.smoke


class ItemWrapper(csr.NamedItem):
    """Wrapper to be able to construct an object."""

    child: ItemWrapper | None

    @property
    def _children(self) -> tuple[csr.NamedItem, ...]:
        """All subitems within item."""
        return (self.child,) if self.child else ()


def build_item(**kwargs: Any) -> ItemWrapper:
    """Create default item."""
    defaults = {
        "name": "some_name",
        "doc": "Some description.",
        "metadata": {},
        "child": None,
    }
    defaults.update(kwargs)
    return ItemWrapper(**defaults)


def test_parent() -> None:
    """Test `parent` field."""
    child = build_item(name="child")
    parent = build_item(name="parent", child=child)

    assert child.parent == parent

    assert str(child.path) == f"{parent.name}.{child.name}"


def test_validation_success() -> None:
    """Test successful validation."""
    item = build_item()
    assert isinstance(item, csr.NamedItem)
    assert item.name == "some_name"
    assert item.doc == "Some description."
    assert isinstance(item.metadata, csr.ItemMetadata)
    assert item.parent is None
    assert str(item.path) == item.name


def test_invalid_name_empty() -> None:
    """Test name is empty."""
    with pytest.raises(ValidationError, match="at least 1 character"):
        build_item(name="")


def test_invalid_name_pattern() -> None:
    """Test name is bad pattern."""
    with pytest.raises(ValidationError, match="should match pattern"):
        build_item(name="123foo")
    with pytest.raises(ValidationError, match="should match pattern"):
        build_item(name="foo-bar")
    with pytest.raises(ValidationError, match="should match pattern"):
        build_item(name="!baz")
    with pytest.raises(ValidationError, match="should match pattern"):
        build_item(name="FOO?")


def test_brief() -> None:
    """Test valid brief."""
    item = build_item(doc="First line\n\nSecond line")
    assert item.brief == "First line"

    item = build_item(doc="First line\nSecond line")
    assert item.brief == "First line"

    item = build_item(doc="First line")
    assert item.brief == "First line"

    item = build_item(doc="   First line   \n\nSecond line")
    assert item.brief == "First line"


def test_description() -> None:
    """Test valid description."""
    item = build_item(doc="First line\n\nSecond line")
    assert item.description == "Second line"

    item = build_item(doc="First line\n\nSecond line\nThird line\n")
    assert item.description == "Second line\nThird line"

    item = build_item(doc="First line\nSecond line")
    assert item.description == "Second line"

    item = build_item(doc="First line")
    assert item.description == "First line"

    item = build_item(doc="   First line   \n\nSecond line   \n")
    assert item.description == "Second line"


def test_metadata() -> None:
    """Test metadata is attached."""
    item = build_item(metadata={"foo": 42})
    assert item.metadata.foo == 42  # type: ignore reportAttributeAccessIssue


def test_string_preprocessing() -> None:
    """Test whitespace stripping and lowercase conversion for string fields."""
    item = build_item(
        name="  ValidName  ",
        doc="  Valid doc \n\n with spaces  ",
    )
    assert item.name == "validname"  # Whitespace stripped and converted to lowercase
    assert item.doc == "Valid doc \n\n with spaces"  # Whitespace stripped only


def test_immutability() -> None:
    """Test item immutability."""
    item = build_item()
    with pytest.raises(ValidationError, match="Instance is frozen"):
        item.name = "bar"


def test_extra_values_forbid() -> None:
    """Test that extra values are not permitted."""
    with pytest.raises(ValidationError, match="Extra inputs are not permitted"):
        ItemWrapper.model_validate({"name": "name", "doc": "doc", "metadata": {}, "the_answer": 42})
