"""Tests for corsair build targets."""

from __future__ import annotations

import pytest
from pydantic import BaseModel, ValidationError

from corsair import (
    AnyTarget,
    CustomTarget,
    MapCHeaderTarget,
    MapMarkdownTarget,
    MapSvPackageTarget,
    MapVerilogHeaderTarget,
    MapVerilogTarget,
    MapVhdlTarget,
)

# All tests below can be used in smoke testing
pytestmark = pytest.mark.smoke


class TargetWrapper(BaseModel):
    """Dummy wrapper to check that field discriminator works."""

    target: AnyTarget


def test_custom_target() -> None:
    """Test that a CustomTarget can be created with a valid generator."""
    data = {"kind": "custom", "generator": "my_generator.py::MyGeneratorClass"}
    target = TargetWrapper.model_validate({"target": data}).target
    assert isinstance(target, CustomTarget)
    assert target.generator == "my_generator.py::MyGeneratorClass"


def test_custom_target_invalid_generator() -> None:
    """Test that CustomTarget raises ValidationError for invalid generator patterns."""
    data = {"kind": "custom", "generator": "invalid_generator"}
    with pytest.raises(ValidationError):
        TargetWrapper.model_validate({"target": data})


def test_map_verilog_target() -> None:
    """Test that a MapVerilogTarget can be created."""
    data = {"kind": "map_verilog"}
    target = TargetWrapper.model_validate({"target": data}).target
    assert isinstance(target, MapVerilogTarget)


def test_map_vhdl_target() -> None:
    """Test that a MapVhdlTarget can be created."""
    data = {"kind": "map_vhdl"}
    target = TargetWrapper.model_validate({"target": data}).target
    assert isinstance(target, MapVhdlTarget)


def test_map_verilog_header_target() -> None:
    """Test that MapVerilogHeaderTarget accepts valid prefixes."""
    data = {"kind": "map_verilog_header", "prefix": "MyPrefix"}
    target = TargetWrapper.model_validate({"target": data}).target
    assert isinstance(target, MapVerilogHeaderTarget)
    assert target.prefix == "myprefix"  # to_lower=True


def test_map_verilog_header_target_invalid_prefix() -> None:
    """Test that MapVerilogHeaderTarget raises ValidationError for invalid prefixes."""
    with pytest.raises(ValidationError):
        TargetWrapper.model_validate({"target": {"kind": "map_verilog_header", "prefix": "1Invalid"}})

    with pytest.raises(ValidationError):
        TargetWrapper.model_validate({"target": {"kind": "map_verilog_header", "prefix": "Invalid-Name"}})

    with pytest.raises(ValidationError):
        TargetWrapper.model_validate({"target": {"kind": "map_verilog_header", "prefix": "Invalid Name"}})

    with pytest.raises(ValidationError):
        TargetWrapper.model_validate({"target": {"kind": "map_verilog_header", "prefix": ""}})


def test_map_c_header_target() -> None:
    """Test that MapCHeaderTarget accepts valid prefixes."""
    data = {"kind": "map_c_header", "prefix": "MyPrefix"}
    target = TargetWrapper.model_validate({"target": data}).target
    assert isinstance(target, MapCHeaderTarget)
    assert target.prefix == "myprefix"  # to_lower=True


def test_map_c_header_target_invalid_prefix() -> None:
    """Test that MapCHeaderTarget raises ValidationError for invalid prefixes."""
    with pytest.raises(ValidationError):
        TargetWrapper.model_validate({"target": {"kind": "map_c_header", "prefix": "Invalid-Name"}})

    with pytest.raises(ValidationError):
        TargetWrapper.model_validate({"target": {"kind": "map_c_header", "prefix": "Invalid Name"}})

    with pytest.raises(ValidationError):
        TargetWrapper.model_validate({"target": {"kind": "map_c_header", "prefix": "123abc"}})

    with pytest.raises(ValidationError):
        TargetWrapper.model_validate({"target": {"kind": "map_c_header", "prefix": ""}})


def test_map_sv_package_target() -> None:
    """Test that MapSvPackageTarget accepts valid prefixes."""
    data = {"kind": "map_sv_package", "prefix": "MyPrefix"}
    target = TargetWrapper.model_validate({"target": data}).target
    assert isinstance(target, MapSvPackageTarget)
    assert target.prefix == "myprefix"  # to_lower=True


def test_map_sv_package_target_invalid_prefix() -> None:
    """Test that MapSvPackageTarget raises ValidationError for invalid prefixes."""
    with pytest.raises(ValidationError):
        TargetWrapper.model_validate({"target": {"kind": "map_sv_package", "prefix": "Invalid-Name"}})

    with pytest.raises(ValidationError):
        TargetWrapper.model_validate({"target": {"kind": "map_sv_package", "prefix": "Invalid Name"}})

    with pytest.raises(ValidationError):
        TargetWrapper.model_validate({"target": {"kind": "map_sv_package", "prefix": "123abc"}})

    with pytest.raises(ValidationError):
        TargetWrapper.model_validate({"target": {"kind": "map_sv_package", "prefix": ""}})


def test_map_markdown_target() -> None:
    """Test that MapMarkdownTarget can be created with custom settings."""
    data = {
        "kind": "map_markdown",
        "title": "My Register Map",
        "print_images": False,
        "print_conventions": False,
    }
    target = TargetWrapper.model_validate({"target": data}).target
    assert isinstance(target, MapMarkdownTarget)
    assert target.title == "My Register Map"
    assert target.print_images == False
    assert target.print_conventions == False


def test_map_markdown_target_defaults() -> None:
    """Test that MapMarkdownTarget uses default values when not provided."""
    data = {"kind": "map_markdown"}
    target = TargetWrapper.model_validate({"target": data}).target
    assert isinstance(target, MapMarkdownTarget)
    assert target.title == "Register map"
    assert target.print_images is True
    assert target.print_conventions is True


def test_invalid_kind() -> None:
    """Test that an invalid 'kind' value raises ValidationError."""
    data = {"kind": "invalid_kind"}
    with pytest.raises(ValidationError):
        TargetWrapper.model_validate({"target": data})
