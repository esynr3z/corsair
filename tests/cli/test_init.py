"""Tests for the `corsair init` command."""

from __future__ import annotations

import json
import logging
import os
from importlib.machinery import ModuleSpec
from pathlib import Path
from typing import TYPE_CHECKING
from unittest import mock

import hjson
import pytest
import yaml
from typer.testing import CliRunner

import corsair as csr
from corsair._app import app
from corsair._app.init import TemplateKind

if TYPE_CHECKING:
    from collections.abc import Callable, Generator


@pytest.fixture
def runner(tmp_path: Path) -> Generator[CliRunner, None, None]:
    """Fixture for invoking command-line interfaces."""
    # Ensure the corsair logger exists and is usable by caplog
    _ = logging.getLogger("corsair")

    original_cwd = Path.cwd()
    os.chdir(tmp_path)
    yield CliRunner(mix_stderr=False)
    os.chdir(original_cwd)


def _check_generated_files(
    cli_runner: CliRunner,
    build_file: Path,
    map_file: Path,
) -> None:
    """Check generated files."""
    assert build_file.exists()
    assert map_file.exists()

    check_result = cli_runner.invoke(app, ["check", str(build_file.resolve()), str(map_file.resolve())])
    assert check_result.exit_code == 0, "Generated files failed 'corsair check'"


def test_init_default_args(runner: CliRunner, tmp_path: Path) -> None:
    """Test `corsair init` with default arguments."""
    result = runner.invoke(app, ["init"])
    assert result.exit_code == 0

    build_file = tmp_path / "csrbuild.yaml"
    map_file = tmp_path / "csrmap.yaml"
    _check_generated_files(runner, build_file, map_file)

    # Verify build spec content defaults
    build_spec = csr.BuildSpecification.from_file(build_file)
    assert build_spec.loader.kind == "yaml"
    assert build_spec.loader.mapfile == Path(
        f"csrmap.{TemplateKind.YAML.value}"
    )  # Default mapfile name based on loader kind

    # Verify map file content (basic check)
    with map_file.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    reg_map = csr.Map.model_validate(data)
    assert reg_map.name == "uart"


@pytest.mark.parametrize(
    "kind",
    [TemplateKind.JSON, TemplateKind.HJSON, TemplateKind.YAML],
)
def test_init_all_kinds(runner: CliRunner, tmp_path: Path, kind: TemplateKind) -> None:
    """Test `corsair init` for each kind."""
    result = runner.invoke(app, ["init", str(kind)])
    assert result.exit_code == 0

    build_file = tmp_path / "csrbuild.yaml"
    map_file = tmp_path / f"csrmap.{kind.value}"
    _check_generated_files(runner, build_file, map_file)

    # Verify build spec content for the specific kind
    build_spec = csr.BuildSpecification.from_file(build_file)
    assert build_spec.loader.kind == str(kind)
    assert build_spec.loader.mapfile == Path("csrmap.yaml")

    # Verify map file content (basic check)
    with map_file.open("r", encoding="utf-8") as f:
        if kind == TemplateKind.JSON:
            data = json.load(f)
        elif kind == TemplateKind.HJSON:
            data = hjson.load(f)
        elif kind == TemplateKind.YAML:
            data = yaml.safe_load(f)
    reg_map = csr.Map.model_validate(data)
    assert reg_map.name == "uart"


def test_init_custom_output_dir(runner: CliRunner, tmp_path: Path) -> None:
    """Test `corsair init` with a custom output directory."""
    custom_dir_name = "custom_project"
    custom_output_dir = tmp_path / custom_dir_name
    # Typer's runner invokes the command from tmp_path, so output path should be relative to it or absolute
    result = runner.invoke(app, ["init", "--output", custom_dir_name])
    assert result.exit_code == 0
    assert custom_output_dir.exists()
    assert custom_output_dir.is_dir()

    build_file = custom_output_dir / "csrbuild.yaml"
    map_file = custom_output_dir / "csrmap.yaml"

    # Check files exist in the custom directory
    assert build_file.exists()
    assert map_file.exists()

    # For _check_generated_files, paths need to be relative to where runner is (tmp_path)
    _check_generated_files(runner, build_file, map_file)


# Helper function to create the side_effect for mocking importlib.util.find_spec
def _create_find_spec_side_effect(
    module_to_mock_as_missing: str,
) -> Callable[[str, str | None], ModuleSpec | None]:
    """Create a side_effect function for mock.patch on importlib.util.find_spec."""

    def side_effect(name: str, _: str | None = None) -> ModuleSpec | None:
        if name == module_to_mock_as_missing:
            return None
        # For other packages, return a mock spec object
        mock_spec = mock.MagicMock(spec=ModuleSpec)
        mock_spec.name = name
        return mock_spec

    return side_effect


@mock.patch("importlib.util.find_spec")
def test_init_no_wavedrom_installed(mock_find_spec: mock.MagicMock, runner: CliRunner, tmp_path: Path) -> None:
    """Test `corsair init` when wavedrom is not installed."""
    mock_find_spec.side_effect = _create_find_spec_side_effect("wavedrom")

    result = runner.invoke(app, ["init"])  # Default kind is YAML
    assert result.exit_code == 0

    build_file = tmp_path / "csrbuild.yaml"
    map_file = tmp_path / "csrmap.yaml"
    _check_generated_files(runner, build_file, map_file)

    # Verify build spec content reflects no wavedrom
    build_spec_data = yaml.safe_load(build_file.read_text())
    assert "doc_wavedrom" not in build_spec_data["generators"]
    assert build_spec_data["generators"]["doc_markdown"]["print_images"] is False


@mock.patch("importlib.util.find_spec")
def test_init_hjson_kind_no_hjson_installed(mock_find_spec: mock.MagicMock, runner: CliRunner) -> None:
    """Test `corsair init hjson` when hjson is not installed."""
    mock_find_spec.side_effect = _create_find_spec_side_effect("hjson")

    result = runner.invoke(app, ["init", "hjson"])
    assert result.exit_code != 0
    assert isinstance(result.exception, ImportError)
    assert "hjson is not installed" in str(result.exception)
