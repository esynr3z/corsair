"""Tests for access mode of a bitfield."""

from __future__ import annotations

import pytest
from pydantic import BaseModel, ValidationError

from corsair import AccessCategory, AccessMode


def test_str() -> None:
    """Test access to string conversion."""
    mode = AccessMode("rw")
    assert str(mode) == "rw" == mode.value
    mode = AccessMode("wosc")
    assert str(mode) == "wosc" == mode.value


def test_repr() -> None:
    """Test access to repr string conversion."""
    mode = AccessMode("rw")
    assert repr(mode) == "<AccessMode.RW: 'rw'>"
    mode = AccessMode("wosc")
    assert repr(mode) == "<AccessMode.WOSC: 'wosc'>"


def test_pydantic_validate() -> None:
    """Test of validation with pydantic model."""

    class Wrapper(BaseModel):
        mode: AccessMode

    model = Wrapper(mode=AccessMode("rw"))
    assert model.mode == AccessMode("rw") == AccessMode.RW

    model = Wrapper.model_validate({"mode": "wo"})
    assert model.mode == AccessMode("wo") == AccessMode.WO

    with pytest.raises(ValidationError, match="Input should be"):
        Wrapper.model_validate({"mode": "we"})


def test_pydantic_dump_json() -> None:
    """Test of dump from pydantic model."""

    class Wrapper(BaseModel):
        mode: AccessMode

    dump = Wrapper(mode=AccessMode("roc")).model_dump_json()
    assert dump == '{"mode":"roc"}'


def test_access_is_ro() -> None:
    """Test is_ro property for different access modes."""
    assert AccessMode.RO.is_ro == True
    assert AccessMode.ROC.is_ro == True
    assert AccessMode.ROLL.is_ro == True
    assert AccessMode.ROLH.is_ro == True
    assert AccessMode.RW.is_ro == False
    assert AccessMode.WO.is_ro == False


def test_access_is_wo() -> None:
    """Test is_wo property for different access modes."""
    assert AccessMode.WO.is_wo == True
    assert AccessMode.WOSC.is_wo == True
    assert AccessMode.RW.is_wo == False
    assert AccessMode.RO.is_wo == False


def test_access_is_rw() -> None:
    """Test is_rw property for different access modes."""
    assert AccessMode.RW.is_rw == True
    assert AccessMode.RW1C.is_rw == True
    assert AccessMode.RW1S.is_rw == True
    assert AccessMode.WO.is_rw == False
    assert AccessMode.WOSC.is_rw == False
    assert AccessMode.RO.is_rw == False


def test_access_invalid_value() -> None:
    """Test that invalid access mode values raise ValueError."""
    with pytest.raises(ValueError, match="is not a valid AccessMode"):
        AccessMode("invalid")
    with pytest.raises(ValueError, match="is not a valid AccessMode"):
        AccessMode("r")
    with pytest.raises(ValueError, match="is not a valid AccessMode"):
        AccessMode("rw1")


def test_access_comparison() -> None:
    """Test comparison operations between Access enum members."""
    assert AccessMode("rw") == AccessMode.RW
    assert AccessMode.RW != AccessMode.WO
    assert AccessMode.RW == "rw"
    assert AccessMode.WO != "rw"


def test_access_category() -> None:
    """Test access category."""
    assert AccessMode.RW.category == AccessCategory.RW
    assert AccessMode.WO.category == AccessCategory.WO
    assert AccessMode.ROC.category == AccessCategory.RO
    assert AccessMode.WOSC.category == AccessCategory.WO
    assert AccessMode.ROLL.category == AccessCategory.RO
    assert AccessMode.ROLH.category == AccessCategory.RO


def test_access_category_str() -> None:
    """Test AccessCategory to string conversion."""
    category = AccessCategory("rw")
    assert str(category) == "rw" == category.value
    category = AccessCategory("ro")
    assert str(category) == "ro" == category.value


def test_access_category_comparison() -> None:
    """Test comparison operations between AccessCategory enum members."""
    assert AccessCategory("rw") == AccessCategory.RW
    assert AccessCategory.RW != AccessCategory.WO
    assert AccessCategory.RW == "rw"
    assert AccessCategory.WO != "rw"


def test_access_category_invalid_value() -> None:
    """Test that invalid access category values raise ValueError."""
    with pytest.raises(ValueError, match="is not a valid AccessCategory"):
        AccessCategory("invalid")
    with pytest.raises(ValueError, match="is not a valid AccessCategory"):
        AccessCategory("r")
    with pytest.raises(ValueError, match="is not a valid AccessCategory"):
        AccessCategory("rw1")
