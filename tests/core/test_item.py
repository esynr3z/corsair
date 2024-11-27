"""Tests base register map item."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from corsair.core.item import StrictModelItem

# All tests below can be used in smoke testing
pytestmark = pytest.mark.smoke


class ItemWrapper(StrictModelItem):
    """Wrapper to be able to construct an object."""


def build_item(
    name: str = "some_name",
    doc: str = "Some description.",
    metadata: dict | None = None,
) -> ItemWrapper:
    """Create default item."""
    return ItemWrapper(
        name=name,
        doc=doc,
        metadata=metadata if metadata else {},
    )


def test_parent() -> None:
    """Test `parent` field."""

    class Parent(StrictModelItem):
        child: ItemWrapper

    child = build_item(name="child")
    parent = Parent(name="parent", doc="", metadata={}, child=child)
    child._assign_parent(parent)

    assert child.parent == parent

    # cannot be changed anymore
    parent2 = Parent(name="parent2", doc="", metadata={}, child=child)
    child._assign_parent(parent2)
    assert child.parent == parent

    assert str(child.path) == f"{parent.name}/{child.name}"


def test_validation_success() -> None:
    """Test successful validation."""
    item = build_item()
    assert isinstance(item, ItemWrapper)
    assert isinstance(item, StrictModelItem)
    assert item.name == "some_name"
    assert item.doc == "Some description."
    assert isinstance(item.metadata, dict)
    assert len(item.metadata) == 0
    with pytest.raises(AttributeError):
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
    assert item.metadata["foo"] == 42


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
