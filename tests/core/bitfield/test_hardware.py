"""Tests hardware mode of a bitfield."""

from __future__ import annotations

import pytest
from pydantic import BaseModel, ValidationError

from corsair import Hardware

# All tests below can be used in smoke testing
pytestmark = pytest.mark.smoke


def test_aliases() -> None:
    """Test for aliases."""
    assert Hardware.INPUT == Hardware.I == Hardware("i") == Hardware("I")
    assert Hardware.OUTPUT == Hardware.O == Hardware("o") == Hardware("O")
    assert Hardware.CLEAR == Hardware.C == Hardware("c") == Hardware("C")
    assert Hardware.SET == Hardware.S == Hardware("s") == Hardware("S")
    assert Hardware.ENABLE == Hardware.E == Hardware("e") == Hardware("E")
    assert Hardware.LOCK == Hardware.L == Hardware("l") == Hardware("L")
    assert Hardware.ACCESS == Hardware.A == Hardware("a") == Hardware("A")
    assert Hardware.QUEUE == Hardware.Q == Hardware("q") == Hardware("Q")
    assert Hardware.FIXED == Hardware.F == Hardware("f") == Hardware("F")
    assert Hardware.NA == Hardware.N == Hardware("n") == Hardware("N")


def test_single_item_operations() -> None:
    """Test operations over single item."""
    mode = Hardware.I
    assert repr(mode) == "<Hardware.INPUT: 'i'>"
    assert str(mode) == "i"
    assert set(mode) == set(Hardware.I)
    assert mode == Hardware.I
    assert mode != Hardware.O
    assert Hardware.I in mode
    assert mode <= Hardware.I
    assert mode >= Hardware.I
    assert not mode < Hardware.I
    assert not mode > Hardware.I
    assert not mode <= Hardware.O
    assert not mode >= Hardware.O
    assert not mode < Hardware.O
    assert not mode > Hardware.O
    assert len(mode) == 1


def test_comb_item_operations() -> None:
    """Test operations over item as a combination of flags."""
    mode = Hardware.I | Hardware.O | Hardware.E
    assert repr(mode) == "<Hardware.INPUT|OUTPUT|ENABLE: 'i-o-e'>"
    assert str(mode) == "i-o-e"
    assert set(mode) == {Hardware.I, Hardware.O, Hardware.E}
    assert Hardware.I in mode
    assert Hardware.O in mode
    assert Hardware.L not in mode
    assert mode != Hardware.I
    assert mode != Hardware.O
    assert mode != Hardware.E
    assert len(mode) == 3

    subset_mode = Hardware.I | Hardware.O
    assert not subset_mode > mode
    assert not subset_mode >= mode
    assert subset_mode < mode
    assert subset_mode <= mode

    superset_mode = Hardware.I | Hardware.O | Hardware.E | Hardware.L
    assert superset_mode > mode
    assert superset_mode >= mode
    assert not superset_mode < mode
    assert not superset_mode <= mode


def test_creation_from_string() -> None:
    """Test creation from literals."""
    mode_io = Hardware("io")
    assert mode_io == (Hardware.I | Hardware.O)
    mode_io = Hardware("ioioio")
    assert mode_io == (Hardware.I | Hardware.O)
    mode_io = Hardware("i-o-e")
    assert mode_io == (Hardware.I | Hardware.O | Hardware.E)
    mode_cs = Hardware("cS")
    assert mode_cs == (Hardware.C | Hardware.S)
    mode_ei = Hardware("EI")
    assert mode_ei == (Hardware.E | Hardware.I)
    mode_n = Hardware("")
    assert mode_n == Hardware.N
    mode_f = Hardware("f")
    assert mode_f == Hardware.F
    mode_q = Hardware("q")
    assert mode_q == Hardware.Q


def test_invalid_string_creation() -> None:
    """Test for unknown flags."""
    with pytest.raises(ValueError, match="Unknown hardware mode"):
        Hardware("x")
    with pytest.raises(ValueError, match="Unknown hardware mode"):
        Hardware("xyz")
    with pytest.raises(ValueError, match="Unknown hardware mode"):
        Hardware("z|i")


def test_single_str_item_operations() -> None:
    """Test operations over a single item represented as a string."""
    mode = Hardware.I
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
    mode = Hardware.I | Hardware.O | Hardware.E
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
    mode = Hardware("")
    assert str(mode) == "n"
    assert mode == Hardware.N


def test_str_conversion() -> None:
    """Test flags to string conversion."""
    mode = Hardware("iocl")
    assert str(mode) == "i-o-c-l" == mode.value
    mode = Hardware("oicl")
    assert str(mode) == "i-o-c-l"
    mode = Hardware("o-i-l-c")
    assert str(mode) == "i-o-c-l"


def test_pydantic_validate() -> None:
    """Test of validation with pydantic model."""

    class Wrapper(BaseModel):
        mode: Hardware

    model = Wrapper(mode=Hardware("i-o"))
    assert model.mode == Hardware("io") == (Hardware.I | Hardware.O)

    model = Wrapper.model_validate({"mode": "f"})
    assert model.mode == Hardware("f") == Hardware.F

    with pytest.raises(ValidationError, match="Input should be"):
        Wrapper.model_validate({"mode": "xyz"})


def test_pydantic_dump_json() -> None:
    """Test of dump from pydantic model."""

    class Wrapper(BaseModel):
        mode: Hardware

    dump = Wrapper(mode=Hardware("io")).model_dump_json()
    assert dump == '{"mode":"i-o"}'
