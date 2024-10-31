"""Tests hardware mode of a bitfield."""

from __future__ import annotations

import pytest
from pydantic import BaseModel

from corsair import HwMode


def test_aliases() -> None:
    """Test for aliases."""
    assert HwMode.INPUT == HwMode.I == HwMode("i") == HwMode("I")
    assert HwMode.OUTPUT == HwMode.O == HwMode("o") == HwMode("O")
    assert HwMode.CLEAR == HwMode.C == HwMode("c") == HwMode("C")
    assert HwMode.SET == HwMode.S == HwMode("s") == HwMode("S")
    assert HwMode.ENABLE == HwMode.E == HwMode("e") == HwMode("E")
    assert HwMode.LOCK == HwMode.L == HwMode("l") == HwMode("L")
    assert HwMode.ACCESS == HwMode.A == HwMode("a") == HwMode("A")
    assert HwMode.QUEUE == HwMode.Q == HwMode("q") == HwMode("Q")
    assert HwMode.FIXED == HwMode.F == HwMode("f") == HwMode("F")
    assert HwMode.NA == HwMode.N == HwMode("n") == HwMode("N")


def test_single_item_operations() -> None:
    """Test operations over single item."""
    mode = HwMode.I
    assert repr(mode) == "<HwMode.INPUT: 'i'>"
    assert str(mode) == "i"
    assert set(mode) == set(HwMode.I)
    assert mode == HwMode.I
    assert mode != HwMode.O
    assert HwMode.I in mode
    assert mode <= HwMode.I
    assert mode >= HwMode.I
    assert not mode < HwMode.I
    assert not mode > HwMode.I
    assert not mode <= HwMode.O
    assert not mode >= HwMode.O
    assert not mode < HwMode.O
    assert not mode > HwMode.O


def test_comb_item_operations() -> None:
    """Test operations over item as a combination of flags."""
    mode = HwMode.I | HwMode.O | HwMode.E
    assert repr(mode) == "<HwMode.INPUT|OUTPUT|ENABLE: 'i|o|e'>"
    assert str(mode) == "i|o|e"
    assert set(mode) == {HwMode.I, HwMode.O, HwMode.E}
    assert HwMode.I in mode
    assert HwMode.O in mode
    assert HwMode.L not in mode
    assert mode != HwMode.I
    assert mode != HwMode.O
    assert mode != HwMode.E

    subset_mode = HwMode.I | HwMode.O
    assert not subset_mode > mode
    assert not subset_mode >= mode
    assert subset_mode < mode
    assert subset_mode <= mode

    superset_mode = HwMode.I | HwMode.O | HwMode.E | HwMode.L
    assert superset_mode > mode
    assert superset_mode >= mode
    assert not superset_mode < mode
    assert not superset_mode <= mode


def test_creation_from_string() -> None:
    """Test creation from literals."""
    mode_io = HwMode("io")
    assert mode_io == (HwMode.I | HwMode.O)
    mode_io = HwMode("ioioio")
    assert mode_io == (HwMode.I | HwMode.O)
    mode_io = HwMode("i|o|e")
    assert mode_io == (HwMode.I | HwMode.O | HwMode.E)
    mode_cs = HwMode("cS")
    assert mode_cs == (HwMode.C | HwMode.S)
    mode_ei = HwMode("EI")
    assert mode_ei == (HwMode.E | HwMode.I)
    mode_n = HwMode("")
    assert mode_n == HwMode.N
    mode_f = HwMode("f")
    assert mode_f == HwMode.F
    mode_q = HwMode("q")
    assert mode_q == HwMode.Q


def test_invalid_string_creation() -> None:
    """Test for unknown flags."""
    with pytest.raises(ValueError, match="Unknown hardware mode"):
        HwMode("x")
    with pytest.raises(ValueError, match="Unknown hardware mode"):
        HwMode("xyz")
    with pytest.raises(ValueError, match="Unknown hardware mode"):
        HwMode("z|i")


def test_single_str_item_operations() -> None:
    """Test operations over a single item represented as a string."""
    mode = HwMode.I
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
    mode = HwMode.I | HwMode.O | HwMode.E
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
    mode = HwMode("")
    assert str(mode) == "n"
    assert mode == HwMode.N


def test_str_conversion() -> None:
    """Test flags to string conversion."""
    mode = HwMode("iocl")
    assert str(mode) == "i|o|c|l" == mode.value
    mode = HwMode("oicl")
    assert str(mode) == "i|o|c|l"
    mode = HwMode("o|i|l|c")
    assert str(mode) == "i|o|c|l"


def test_pydantic_validate() -> None:
    """Test of validation with pydantic model."""

    class Wrapper(BaseModel):
        mode: HwMode

    model = Wrapper(mode=HwMode("i|o"))
    assert model.mode == HwMode("io") == (HwMode.I | HwMode.O)


def test_pydantic_dump_json() -> None:
    """Test of dump from pydantic model."""

    class Wrapper(BaseModel):
        mode: HwMode

    dump = Wrapper(mode=HwMode("io")).model_dump_json()
    assert dump == '{"mode":"i|o"}'
