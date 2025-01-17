"""Tests for a build related functionality."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

import corsair as csr

# All tests below can be used in smoke testing
pytestmark = pytest.mark.smoke


def test_empty_spec() -> None:
    """Test empty build specification."""
    with pytest.raises(ValueError, match="Field required"):
        csr.BuildSpecification()  # type: ignore reportCallIssue


def test_minimal_spec() -> None:
    """Test minimal build specification."""
    data = {"generators": [{"kind": "verilog"}]}
    spec = csr.BuildSpecification.model_validate(data)
    assert spec.parser.kind == "yaml"
    assert len(spec.generators) == 1
    assert spec.generators[0].kind == "verilog"
    assert isinstance(spec.parser, csr.Deserializer.Config)
    assert isinstance(spec.generators[0], csr.VerilogGenerator.Config)


def test_full_spec() -> None:
    """Test full build specification."""
    data = {
        "parser": {"kind": "json", "mapfile": "map.json"},
        "generators": [
            {"kind": "verilog", "use_map": "main", "label": "rtl"},
            {"kind": "vhdl", "use_map": "main"},
        ],
    }
    spec = csr.BuildSpecification.model_validate(data)
    assert spec.parser.kind == "json"
    assert spec.parser.mapfile == Path("map.json")
    assert len(spec.generators) == 2
    assert spec.generators[0].label == "rtl"
    assert spec.generators[1].label == "vhdl"


def test_forbidden_extra() -> None:
    """Test adding forbidden extra fields to specification."""
    data = {"extra": "value", "generators": [{"kind": "verilog", "use_map": "main"}]}
    with pytest.raises(ValueError, match="Extra inputs are not permitted"):
        csr.BuildSpecification.model_validate(data)


def test_empty_generators() -> None:
    """Test that empty generators are not allowed."""
    data = {"generators": []}
    with pytest.raises(ValueError, match="List should have at least 1 item"):
        csr.BuildSpecification.model_validate(data)


def test_empty_parser() -> None:
    """Test that empty parser leads to creation of default YAML parser."""
    data = {"generators": [{"kind": "verilog"}]}
    spec = csr.BuildSpecification.model_validate(data)
    assert isinstance(spec.parser, csr.Deserializer.Config)
    assert spec.parser.kind == "yaml"
    assert spec.parser.mapfile == Path("csrmap.yaml")


def test_unique_generators() -> None:
    """Test that generators labels are unique."""
    data = {"generators": [{"kind": "verilog"}, {"kind": "verilog"}]}
    with pytest.raises(ValueError, match="Generator labels must be unique"):
        csr.BuildSpecification.model_validate(data)

    data = {"generators": [{"kind": "verilog", "label": "rtl1"}, {"kind": "verilog", "label": "rtl2"}]}
    spec = csr.BuildSpecification.model_validate(data)
    assert spec.generators[0].label == "rtl1"
    assert spec.generators[1].label == "rtl2"


def test_wrong_parser() -> None:
    """Test that wrong parser raises error."""
    data = {"parser": {"kind": "wrong"}, "generators": [{"kind": "verilog"}]}
    with pytest.raises(ValueError, match="does not match any of the expected tags"):
        csr.BuildSpecification.model_validate(data)


def test_wrong_generator() -> None:
    """Test that wrong generator raises error."""
    data = {"generators": [{"kind": "wrong"}, {"kind": "verilog"}]}
    with pytest.raises(ValueError, match="does not match any of the expected tags"):
        csr.BuildSpecification.model_validate(data)


def test_from_toml(tmp_path: Path) -> None:
    """Test loading specification from TOML file."""
    toml_content = """
    [parser]
    kind = "json"

    [[generators]]
    kind = "verilog"
    label = "rtl"

    [[generators]]
    kind = "vhdl"
    use_map = "main"
    """
    toml_file = tmp_path / "build.toml"
    toml_file.write_text(toml_content)

    spec = csr.BuildSpecification.from_toml_file(toml_file)
    assert spec.parser.kind == "json"
    assert len(spec.generators) == 2
    assert spec.generators[0].label == "rtl"


def test_to_json_schema(tmp_path: Path) -> None:
    """Test writing JSON schema to file."""
    schema_file = tmp_path / "schema.json"
    csr.BuildSpecification.to_json_schema_file(schema_file)

    with schema_file.open() as f:
        schema = json.load(f)

    assert schema["title"] == "BuildSpecification"
    assert "parser" in schema["properties"]
    assert "generators" in schema["properties"]
