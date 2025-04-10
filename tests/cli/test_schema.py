"""Tests for the `corsair schema` command."""

from __future__ import annotations

import json
import re
from typing import TYPE_CHECKING

import pytest
from typer.testing import CliRunner

import corsair as csr
from corsair._app import app

if TYPE_CHECKING:
    from pathlib import Path


@pytest.fixture
def runner() -> CliRunner:
    """CLI runner fixture."""
    return CliRunner(mix_stderr=False)


def test_schema_build_stdout(runner: CliRunner) -> None:
    """Test `schema build` command printing to stdout."""
    result = runner.invoke(app, ["schema", "build"])
    assert result.exit_code == 0
    expected_schema = csr.BuildSpecification.model_json_schema()
    assert json.loads(result.stdout) == expected_schema


def test_schema_map_stdout(runner: CliRunner) -> None:
    """Test `schema map` command printing to stdout."""
    result = runner.invoke(app, ["schema", "map"])
    assert result.exit_code == 0
    expected_schema = csr.Map.model_json_schema()
    assert json.loads(result.stdout) == expected_schema


def test_schema_build_stdout_indent(runner: CliRunner) -> None:
    """Test `schema build --indent` command printing to stdout."""
    result = runner.invoke(app, ["schema", "build", "--indent", "4"])
    assert result.exit_code == 0
    expected_schema = csr.BuildSpecification.model_json_schema()
    # Check if output is valid JSON and matches the schema structure
    assert json.loads(result.stdout) == expected_schema
    # Check if indentation is applied
    lines = result.stdout.strip().split("\n")
    assert len(lines) > 1  # Ensure there are multiple lines
    # Check that lines after the first one are indented
    assert any(re.match(r"^\s{4}[^\s]", line) for line in lines[1:])


def test_schema_map_stdout_indent(runner: CliRunner) -> None:
    """Test `schema map --indent` command printing to stdout."""
    result = runner.invoke(app, ["schema", "map", "--indent", "2"])
    assert result.exit_code == 0
    expected_schema = csr.Map.model_json_schema()
    assert json.loads(result.stdout) == expected_schema
    # Check if indentation is applied
    lines = result.stdout.strip().split("\n")
    assert len(lines) > 1  # Ensure there are multiple lines
    # Check that lines after the first one are indented
    assert any(re.match(r"^\s{2}[^\s]", line) for line in lines[1:])


def test_schema_build_outfile(runner: CliRunner, tmp_path: Path) -> None:
    """Test `schema build --out` command writing to a file."""
    outfile = tmp_path / "build_schema.json"
    result = runner.invoke(app, ["schema", "build", "--out", str(outfile)])
    assert result.exit_code == 0
    assert outfile.exists()
    with outfile.open() as f:
        data = json.load(f)
    expected_schema = csr.BuildSpecification.model_json_schema()
    assert data == expected_schema


def test_schema_map_outfile(runner: CliRunner, tmp_path: Path) -> None:
    """Test `schema map --out` command writing to a file."""
    outfile = tmp_path / "map_schema.json"
    result = runner.invoke(app, ["schema", "map", "--out", str(outfile)])
    assert result.exit_code == 0
    assert outfile.exists()
    with outfile.open() as f:
        data = json.load(f)
    expected_schema = csr.Map.model_json_schema()
    assert data == expected_schema


def test_schema_build_outfile_indent(runner: CliRunner, tmp_path: Path) -> None:
    """Test `schema build --out --indent` command writing to a file."""
    outfile = tmp_path / "build_schema_indent.json"
    result = runner.invoke(app, ["schema", "build", "--out", str(outfile), "--indent", "4"])
    assert result.exit_code == 0
    assert outfile.exists()
    with outfile.open() as f:
        content = f.read()
        data = json.loads(content)
    expected_schema = csr.BuildSpecification.model_json_schema()
    assert data == expected_schema
    # Check for indentation in the file content
    lines = content.strip().split("\n")
    assert len(lines) > 1
    assert any(re.match(r"^\s{4}[^\s]", line) for line in lines[1:])


def test_schema_map_outfile_indent(runner: CliRunner, tmp_path: Path) -> None:
    """Test `schema map --out --indent` command writing to a file."""
    outfile = tmp_path / "map_schema_indent.json"
    result = runner.invoke(app, ["schema", "map", "--out", str(outfile), "--indent", "2"])
    assert result.exit_code == 0
    assert outfile.exists()
    with outfile.open() as f:
        content = f.read()
        data = json.loads(content)
    expected_schema = csr.Map.model_json_schema()
    assert data == expected_schema
    # Check for indentation in the file content
    lines = content.strip().split("\n")
    assert len(lines) > 1
    assert any(re.match(r"^\s{2}[^\s]", line) for line in lines[1:])


def test_schema_invalid_kind(runner: CliRunner) -> None:
    """Test `schema` command with an invalid kind."""
    result = runner.invoke(app, ["schema", "invalid_kind"])
    assert result.exit_code != 0
    # Check for the specific error message from Typer
    assert "Invalid value for 'KIND:{build|map}'" in result.stderr
