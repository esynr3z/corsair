"""Tests access mode of a bitfield."""

from __future__ import annotations

import pytest
from pydantic import BaseModel, ValidationError

from corsair import Access

# All tests below can be used in smoke testing
pytestmark = pytest.mark.smoke


def test_str() -> None:
    """Test access to string conversion."""
    mode = Access("rw")
    assert str(mode) == "rw" == mode.value
    mode = Access("wosc")
    assert str(mode) == "wosc" == mode.value


def test_repr() -> None:
    """Test access to repr string conversion."""
    mode = Access("rw")
    assert repr(mode) == "<Access.RW: 'rw'>"
    mode = Access("wosc")
    assert repr(mode) == "<Access.WOSC: 'wosc'>"


def test_pydantic_validate() -> None:
    """Test of validation with pydantic model."""

    class Wrapper(BaseModel):
        mode: Access

    model = Wrapper(mode=Access("rw"))
    assert model.mode == Access("rw") == Access.RW

    model = Wrapper.model_validate({"mode": "wo"})
    assert model.mode == Access("wo") == Access.WO

    with pytest.raises(ValidationError, match="Input should be"):
        Wrapper.model_validate({"mode": "we"})


def test_pydantic_dump_json() -> None:
    """Test of dump from pydantic model."""

    class Wrapper(BaseModel):
        mode: Access

    dump = Wrapper(mode=Access("roc")).model_dump_json()
    assert dump == '{"mode":"roc"}'
