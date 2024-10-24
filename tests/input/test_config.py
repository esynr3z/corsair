"""Tests for corsair input configuration."""

from __future__ import annotations

from pathlib import Path

import pytest
from pydantic import ValidationError

from corsair import ForceNameCase, GlobalConfig, RegisterReset

# All tests below can be used in smoke testing
pytestmark = pytest.mark.smoke


def test_default_config() -> None:
    """Test that a default GlobalConfig instance can be created with all fields."""
    config = GlobalConfig()
    assert config.regmap == Path("csrmap.yaml")
    assert config.regmap_parser is None
    assert config.base_address == 0
    assert config.data_width == 32
    assert config.address_width == 16
    assert config.register_reset == RegisterReset.SYNC_POS
    assert config.address_increment == False
    assert config.address_alignment == True
    assert config.force_name_case == ForceNameCase.CURRENT


def test_valid_config() -> None:
    """Test that a valid GlobalConfig instance can be created with all fields."""
    config = GlobalConfig(
        regmap=Path("path/to/regmap"),
        regmap_parser="parser.py::ParserClass",
        base_address=0,
        data_width=64,
        address_width=32,
        register_reset=RegisterReset.SYNC_POS,
        address_increment=4,
        address_alignment=True,
        force_name_case=ForceNameCase.CURRENT,
    )
    assert config.regmap == Path("path/to/regmap")
    assert config.regmap_parser == "parser.py::ParserClass"
    assert config.base_address == 0
    assert config.data_width == 64
    assert config.address_width == 32
    assert config.register_reset == RegisterReset.SYNC_POS
    assert config.address_increment == 4
    assert config.address_alignment == True
    assert config.force_name_case == ForceNameCase.CURRENT


def test_regmap_parser_none() -> None:
    """Test that regmap_parser can be None."""
    config = GlobalConfig(regmap_parser=None)
    assert config.regmap_parser is None


def test_regmap_parser_valid_pattern() -> None:
    """Test that regmap_parser accepts valid patterns."""
    config = GlobalConfig(regmap_parser="parser.py::ParserClass")
    assert config.regmap_parser == "parser.py::ParserClass"

    config = GlobalConfig(regmap_parser="foo.py::Foo")
    assert config.regmap_parser == "foo.py::Foo"

    config = GlobalConfig(regmap_parser="some/path/bar.py::BarParser")
    assert config.regmap_parser == "some/path/bar.py::BarParser"


def test_regmap_parser_invalid_pattern() -> None:
    """Test that regmap_parser rejects invalid patterns."""
    with pytest.raises(ValidationError):
        GlobalConfig(regmap_parser="parser.py")

    with pytest.raises(ValidationError):
        GlobalConfig(regmap_parser="::ParserClass")

    with pytest.raises(ValidationError):
        GlobalConfig(regmap_parser="parser::ParserClass")

    with pytest.raises(ValidationError):
        GlobalConfig(regmap_parser="parser.py::")


def test_address_increment_bool() -> None:
    """Test that address_increment accepts boolean values."""
    config = GlobalConfig(address_increment=True)
    assert config.address_increment == True

    config = GlobalConfig(address_increment=False)
    assert config.address_increment == False


def test_address_increment_positive_int() -> None:
    """Test that address_increment accepts positive integers."""
    config = GlobalConfig(address_increment=1)
    assert config.address_increment == 1

    config = GlobalConfig(address_increment=4)
    assert config.address_increment == 4


def test_address_increment_invalid_values() -> None:
    """Test that address_increment rejects invalid values."""
    with pytest.raises(ValidationError):
        GlobalConfig(address_increment=-1)

    with pytest.raises(ValidationError):
        GlobalConfig(address_increment=0)


def test_address_alignment_bool() -> None:
    """Test that address_alignment accepts boolean values."""
    config = GlobalConfig(address_alignment=True)
    assert config.address_alignment == True

    config = GlobalConfig(address_alignment=False)
    assert config.address_alignment == False


def test_address_alignment_positive_int() -> None:
    """Test that address_alignment accepts positive integers."""
    config = GlobalConfig(address_alignment=1)
    assert config.address_alignment == 1

    config = GlobalConfig(address_alignment=4)
    assert config.address_alignment == 4


def test_address_alignment_invalid_values() -> None:
    """Test that address_alignment rejects invalid values."""
    with pytest.raises(ValidationError):
        GlobalConfig(address_alignment=-1)

    with pytest.raises(ValidationError):
        GlobalConfig(address_alignment=0)


def test_data_width_positive_int() -> None:
    """Test that data_width accepts positive integers."""
    config = GlobalConfig(data_width=8)
    assert config.data_width == 8

    config = GlobalConfig(data_width=32)
    assert config.data_width == 32


def test_data_width_invalid_values() -> None:
    """Test that data_width rejects invalid values."""
    with pytest.raises(ValidationError):
        GlobalConfig(data_width=0)

    with pytest.raises(ValidationError):
        GlobalConfig(data_width=-1)


def test_register_reset_enum() -> None:
    """Test that register_reset accepts valid enum values."""
    config = GlobalConfig(register_reset=RegisterReset.SYNC_POS)
    assert config.register_reset == "sync_pos"

    config = GlobalConfig(register_reset=RegisterReset.SYNC_NEG)
    assert config.register_reset == "sync_neg"

    config = GlobalConfig(register_reset=RegisterReset.ASYNC_POS)
    assert config.register_reset == "async_pos"

    config = GlobalConfig(register_reset=RegisterReset.ASYNC_NEG)
    assert config.register_reset == "async_neg"


def test_register_reset_invalid_value() -> None:
    """Test that register_reset rejects invalid values."""
    with pytest.raises(ValidationError):
        GlobalConfig(register_reset="invalid_rst")  # pyright: ignore [reportArgumentType]


def test_force_name_case_enum() -> None:
    """Test that force_name_case accepts valid enum values."""
    config = GlobalConfig(force_name_case=ForceNameCase.CURRENT)
    assert config.force_name_case == "current"

    config = GlobalConfig(force_name_case=ForceNameCase.LOWER)
    assert config.force_name_case == "lower"

    config = GlobalConfig(force_name_case=ForceNameCase.UPPER)
    assert config.force_name_case == "upper"


def test_force_name_case_invalid_value() -> None:
    """Test that force_name_case rejects invalid values."""
    with pytest.raises(ValidationError):
        GlobalConfig(force_name_case="invalid")  # pyright: ignore [reportArgumentType]
