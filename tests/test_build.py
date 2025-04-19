"""Tests for a build related functionality."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

import corsair as csr


def test_empty_spec() -> None:
    """Test empty build specification."""
    with pytest.raises(ValueError, match="Field required"):
        csr.BuildSpecification()  # type: ignore reportCallIssue


def test_minimal_spec() -> None:
    """Test minimal build specification."""
    data = {"generators": {"vlog": {"kind": "verilog"}}}
    spec = csr.BuildSpecification.model_validate(data)
    assert spec.loader.kind == "yaml"
    assert len(spec.generators) == 1
    assert spec.generators["vlog"].kind == "verilog"
    assert isinstance(spec.loader, csr.SerializedLoader.Config)
    assert isinstance(spec.generators["vlog"], csr.VerilogGenerator.Config)


def test_full_spec() -> None:
    """Test full build specification."""
    data = {
        "loader": {"kind": "json", "mapfile": "map.json"},
        "generators": {
            "vlog": {"kind": "verilog"},
            "vhdl": {"kind": "vhdl"},
        },
    }
    spec = csr.BuildSpecification.model_validate(data)
    assert spec.loader.kind == "json"
    assert spec.loader.mapfile == Path("map.json")
    assert len(spec.generators) == 2
    assert spec.generators["vlog"].kind == "verilog"
    assert spec.generators["vhdl"].kind == "vhdl"


def test_forbidden_extra() -> None:
    """Test adding forbidden extra fields to specification."""
    data = {"extra": "value", "generators": [{"kind": "verilog"}]}
    with pytest.raises(ValueError, match="Extra inputs are not permitted"):
        csr.BuildSpecification.model_validate(data)


def test_empty_generators() -> None:
    """Test that empty generators are not allowed."""
    data = {"generators": {}}
    with pytest.raises(ValueError, match="Dictionary should have at least 1 item"):
        csr.BuildSpecification.model_validate(data)


def test_empty_loader() -> None:
    """Test that empty loader leads to creation of default YAML loader."""
    data = {"generators": {"vlog": {"kind": "verilog"}}}
    spec = csr.BuildSpecification.model_validate(data)
    assert isinstance(spec.loader, csr.SerializedLoader.Config)
    assert spec.loader.kind == "yaml"
    assert spec.loader.mapfile == Path("csrmap.yaml")


def test_wrong_loader() -> None:
    """Test that wrong loader raises error."""
    data = {"loader": {"kind": "wrong"}, "generators": {"vlog": {"kind": "verilog"}}}
    with pytest.raises(ValueError, match="does not match any of the expected tags"):
        csr.BuildSpecification.model_validate(data)


def test_wrong_generator() -> None:
    """Test that wrong generator raises error."""
    data = {"generators": {"vlog": {"kind": "wrong"}}}
    with pytest.raises(ValueError, match="does not match any of the expected tags"):
        csr.BuildSpecification.model_validate(data)


def test_from_toml(tmp_path: Path) -> None:
    """Test loading specification from YAML file."""
    yaml_content = """
    loader:
      kind: json

    generators:
      vlog:
        kind: verilog
      vhdl:
        kind: vhdl
    """
    yaml_file = tmp_path / "build.yaml"
    yaml_file.write_text(yaml_content)

    spec = csr.BuildSpecification.from_file(yaml_file)
    assert spec.loader.kind == "json"
    assert len(spec.generators) == 2
    assert spec.generators["vlog"].kind == "verilog"


def test_to_json_schema(tmp_path: Path) -> None:
    """Test writing JSON schema to file."""
    schema_file = tmp_path / "schema.json"
    csr.BuildSpecification.to_json_schema_file(schema_file)

    with schema_file.open() as f:
        schema = json.load(f)

    assert schema["title"] == "BuildSpecification"
    assert "loader" in schema["properties"]
    assert "generators" in schema["properties"]
