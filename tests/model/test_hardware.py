"""Tests for hardware mode of a bitfield."""

from __future__ import annotations

import pytest
from pydantic import BaseModel, ValidationError

from corsair.model import HardwareMode

# All tests below can be used in smoke testing
pytestmark = pytest.mark.smoke


def test_aliases() -> None:
    """Test for aliases."""
    assert HardwareMode.INPUT == HardwareMode.I == HardwareMode("i") == HardwareMode("I")
    assert HardwareMode.OUTPUT == HardwareMode.O == HardwareMode("o") == HardwareMode("O")
    assert HardwareMode.CLEAR == HardwareMode.C == HardwareMode("c") == HardwareMode("C")
    assert HardwareMode.SET == HardwareMode.S == HardwareMode("s") == HardwareMode("S")
    assert HardwareMode.ENABLE == HardwareMode.E == HardwareMode("e") == HardwareMode("E")
    assert HardwareMode.LOCK == HardwareMode.L == HardwareMode("l") == HardwareMode("L")
    assert HardwareMode.ACCESS == HardwareMode.A == HardwareMode("a") == HardwareMode("A")
    assert HardwareMode.QUEUE == HardwareMode.Q == HardwareMode("q") == HardwareMode("Q")
    assert HardwareMode.FIXED == HardwareMode.F == HardwareMode("f") == HardwareMode("F")
    assert HardwareMode.NA == HardwareMode.N == HardwareMode("n") == HardwareMode("N")


def test_single_item_operations() -> None:
    """Test operations over single item."""
    mode = HardwareMode.I
    assert repr(mode) == "<HardwareMode.INPUT: 'i'>"
    assert str(mode) == "i"
    assert set(mode) == set(HardwareMode.I)
    assert mode == HardwareMode.I
    assert mode != HardwareMode.O
    assert HardwareMode.I in mode
    assert mode <= HardwareMode.I
    assert mode >= HardwareMode.I
    assert not mode < HardwareMode.I
    assert not mode > HardwareMode.I
    assert not mode <= HardwareMode.O
    assert not mode >= HardwareMode.O
    assert not mode < HardwareMode.O
    assert not mode > HardwareMode.O
    assert len(mode) == 1


def test_comb_item_operations() -> None:
    """Test operations over item as a combination of flags."""
    mode = HardwareMode.I | HardwareMode.O | HardwareMode.E
    assert repr(mode) == "<HardwareMode.INPUT|OUTPUT|ENABLE: 'i-o-e'>"
    assert str(mode) == "i-o-e"
    assert set(mode) == {HardwareMode.I, HardwareMode.O, HardwareMode.E}
    assert HardwareMode.I in mode
    assert HardwareMode.O in mode
    assert HardwareMode.L not in mode
    assert mode != HardwareMode.I
    assert mode != HardwareMode.O
    assert mode != HardwareMode.E
    assert len(mode) == 3

    subset_mode = HardwareMode.I | HardwareMode.O
    assert not subset_mode > mode
    assert not subset_mode >= mode
    assert subset_mode < mode
    assert subset_mode <= mode

    superset_mode = HardwareMode.I | HardwareMode.O | HardwareMode.E | HardwareMode.L
    assert superset_mode > mode
    assert superset_mode >= mode
    assert not superset_mode < mode
    assert not superset_mode <= mode


def test_creation_from_string() -> None:
    """Test creation from literals."""
    mode_io = HardwareMode("io")
    assert mode_io == (HardwareMode.I | HardwareMode.O)
    mode_io = HardwareMode("ioioio")
    assert mode_io == (HardwareMode.I | HardwareMode.O)
    mode_io = HardwareMode("i-o-e")
    assert mode_io == (HardwareMode.I | HardwareMode.O | HardwareMode.E)
    mode_cs = HardwareMode("cS")
    assert mode_cs == (HardwareMode.C | HardwareMode.S)
    mode_ei = HardwareMode("EI")
    assert mode_ei == (HardwareMode.E | HardwareMode.I)
    mode_n = HardwareMode("")
    assert mode_n == HardwareMode.N
    mode_f = HardwareMode("f")
    assert mode_f == HardwareMode.F
    mode_q = HardwareMode("q")
    assert mode_q == HardwareMode.Q


def test_invalid_string_creation() -> None:
    """Test for unknown flags."""
    with pytest.raises(ValueError, match="Unknown hardware mode"):
        HardwareMode("x")
    with pytest.raises(ValueError, match="Unknown hardware mode"):
        HardwareMode("xyz")
    with pytest.raises(ValueError, match="Unknown hardware mode"):
        HardwareMode("z|i")


def test_single_str_item_operations() -> None:
    """Test operations over a single item represented as a string."""
    mode = HardwareMode.I
    assert "i" in mode
    assert mode <= "i"
    assert mode >= "i"
    assert not mode < "i"
    assert not mode > "i"
    assert not mode <= "o"
    assert not mode >= "o"
    assert not mode < "o"
    assert not mode > "o"


def test_comb_str_item_operations() -> None:
    """Test operations over a string item as a combination of flags."""
    mode = HardwareMode.I | HardwareMode.O | HardwareMode.E
    assert "i" in mode
    assert "o" in mode
    assert "io" in mode
    assert "ioe" in mode
    assert "l" not in mode
    assert "ioel" not in mode

    subset = "io"
    assert not subset > mode
    assert not subset >= mode
    assert subset < mode
    assert subset <= mode

    superset = "ioel"
    assert superset > mode
    assert superset >= mode
    assert not superset < mode
    assert not superset <= mode


def test_na_flag_from_str() -> None:
    """Test for NA flag."""
    mode = HardwareMode("")
    assert str(mode) == "n"
    assert mode == HardwareMode.N


def test_str_conversion() -> None:
    """Test flags to string conversion."""
    mode = HardwareMode("iocl")
    assert str(mode) == "i-o-c-l" == mode.value
    mode = HardwareMode("oicl")
    assert str(mode) == "i-o-c-l"
    mode = HardwareMode("o-i-l-c")
    assert str(mode) == "i-o-c-l"


def test_pydantic_validate() -> None:
    """Test of validation with pydantic model."""

    class Wrapper(BaseModel):
        mode: HardwareMode

    model = Wrapper(mode=HardwareMode("i-o"))
    assert model.mode == HardwareMode("io") == (HardwareMode.I | HardwareMode.O)

    model = Wrapper.model_validate({"mode": "f"})
    assert model.mode == HardwareMode("f") == HardwareMode.F

    with pytest.raises(ValidationError, match="Input should be"):
        Wrapper.model_validate({"mode": "xyz"})


def test_pydantic_dump_json() -> None:
    """Test of dump from pydantic model."""

    class Wrapper(BaseModel):
        mode: HardwareMode

    dump = Wrapper(mode=HardwareMode("io")).model_dump_json()
    assert dump == '{"mode":"i-o"}'


def test_hash_operations() -> None:
    """Test that HardwareMode objects can be used in sets and as dict keys."""
    mode1 = HardwareMode.I | HardwareMode.O
    mode2 = HardwareMode("io")
    mode3 = HardwareMode.O | HardwareMode.I

    # Test set operations
    modes = {mode1, mode2, mode3}
    assert len(modes) == 1  # All modes are equal, should be only one unique value

    # Test dict operations
    modes_dict = {mode1: "first", mode2: "second"}
    assert len(modes_dict) == 1  # Should overwrite due to equal hash
