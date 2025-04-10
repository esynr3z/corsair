"""Tests for the `corsair check` command."""

from __future__ import annotations

import importlib
import logging
import shutil
from pathlib import Path
from typing import TYPE_CHECKING

import pytest
from typer.testing import CliRunner

if TYPE_CHECKING:
    from collections.abc import Generator

from corsair._app import app

HJSON_INSTALLED = importlib.util.find_spec("hjson") is not None  # type: ignore reportAttributeAccessIssue


@pytest.fixture
def runner(tmp_path: Path) -> Generator[CliRunner, None, None]:
    """Fixture for invoking command-line interfaces."""
    # Change CWD for the test to isolate file discovery
    import os

    # Ensure the corsair logger exists and is usable by caplog
    _ = logging.getLogger("corsair")

    original_cwd = Path.cwd()
    os.chdir(tmp_path)
    yield CliRunner(mix_stderr=False)
    os.chdir(original_cwd)


@pytest.fixture
def valid_build_file(tmp_path: Path) -> Path:
    """Fixture for a valid build file."""
    src = Path(__file__).parent / "data" / "valid.csrbuild.toml"
    dst = tmp_path / "valid.csrbuild.toml"
    shutil.copy(src, dst)
    return dst


@pytest.fixture
def invalid_build_file(tmp_path: Path) -> Path:
    """Fixture for an invalid build file."""
    src = Path(__file__).parent / "data" / "invalid.csrbuild.toml"
    dst = tmp_path / "invalid.csrbuild.toml"
    shutil.copy(src, dst)
    return dst


@pytest.fixture(params=["json", "toml", "yaml", "hjson"])
def valid_map_file(tmp_path: Path, request: pytest.FixtureRequest) -> Path:
    """Fixture for a valid map file (parametrized)."""
    ext = request.param
    if ext == "hjson" and not HJSON_INSTALLED:
        pytest.skip("hjson not installed")

    src = Path(__file__).parent / "data" / f"valid.csrmap.{ext}"
    dst = tmp_path / f"valid.csrmap.{ext}"
    shutil.copy(src, dst)
    return dst


@pytest.fixture(params=["json", "toml", "yaml", "hjson"])
def invalid_map_file(tmp_path: Path, request: pytest.FixtureRequest) -> Path:
    """Fixture for an invalid map file (parametrized)."""
    ext = request.param
    if ext == "hjson" and not HJSON_INSTALLED:
        pytest.skip("hjson not installed")

    src = Path(__file__).parent / "data" / f"invalid.csrmap.{ext}"
    dst = tmp_path / f"invalid.csrmap.{ext}"
    shutil.copy(src, dst)
    return dst


@pytest.fixture
def all_valid_files(tmp_path: Path) -> list[Path]:
    """Fixture for all valid files."""
    data_dir = Path(__file__).parent / "data"
    data_files = [f for f in data_dir.glob("valid.*") if "hjson" not in f.name]
    for f in data_files:
        shutil.copy(f, tmp_path / f.name)
    return data_files


@pytest.fixture
def all_invalid_files(tmp_path: Path) -> list[Path]:
    """Fixture for all invalid files."""
    data_dir = Path(__file__).parent / "data"
    data_files = [f for f in data_dir.glob("invalid.*") if "hjson" not in f.name]
    for f in data_files:
        shutil.copy(f, tmp_path / f.name)
    return data_files


def test_check_no_args_no_files(runner: CliRunner) -> None:
    """Test check with no args and no files in CWD."""
    result = runner.invoke(app, ["check"])
    assert result.exit_code != 0
    assert isinstance(result.exception, FileNotFoundError)
    assert "No Corsair files found" in str(result.exception)


def test_check_no_args_only_unsupported(runner: CliRunner, tmp_path: Path) -> None:
    """Test check with no args and only unsupported files."""
    (tmp_path / "file.txt").touch()
    (tmp_path / "another.log").touch()
    result = runner.invoke(app, ["check"])
    assert result.exit_code != 0
    assert isinstance(result.exception, FileNotFoundError)
    assert "No Corsair files found" in str(result.exception)


def test_check_no_args_valid_build(runner: CliRunner, valid_build_file: Path) -> None:  # noqa: ARG001
    """Test check with no args and a valid build file."""
    result = runner.invoke(app, ["check"])
    assert "Found 1 Corsair file" in result.stderr
    assert result.exit_code == 0
    # FIXME: This is not working, because output is wrapped and name is splitted
    # assert valid_build_file.name in result.stderr
    assert result.stderr.count(": OK") == 1


def test_check_no_args_invalid_build(runner: CliRunner, invalid_build_file: Path) -> None:  # noqa: ARG001
    """Test check with no args and an invalid build file."""
    result = runner.invoke(app, ["check"])
    assert "Found 1 Corsair file" in result.stderr
    assert result.exit_code != 0
    assert isinstance(result.exception, RuntimeError)
    # FIXME: This is not working, because output is wrapped and name is splitted
    # assert invalid_build_file.name in result.stderr
    assert result.stderr.count(": FAIL") == 1


def test_check_no_args_valid_map(runner: CliRunner, valid_map_file: Path) -> None:  # noqa: ARG001
    """Test check with no args and a valid map file."""
    result = runner.invoke(app, ["check"])
    assert "Found 1 Corsair file" in result.stderr
    assert result.exit_code == 0
    # FIXME: This is not working, because output is wrapped and name is splitted
    # assert valid_map_file.name in result.stderr
    assert result.stderr.count(": OK") == 1


def test_check_no_args_invalid_map(runner: CliRunner, invalid_map_file: Path) -> None:  # noqa: ARG001
    """Test check with no args and an invalid map file."""
    result = runner.invoke(app, ["check"])
    assert "Found 1 Corsair file" in result.stderr
    assert result.exit_code != 0
    assert isinstance(result.exception, RuntimeError)
    # FIXME: This is not working, because output is wrapped and name is splitted
    # assert invalid_map_file.name in result.stderr
    assert result.stderr.count(": FAIL") == 1


def test_check_no_args_valid_multiple(runner: CliRunner, all_valid_files: list[Path]) -> None:
    """Test check with no args and multiple valid files."""
    result = runner.invoke(app, ["check"])
    assert f"Found {len(all_valid_files)} Corsair file" in result.stderr
    assert result.exit_code == 0
    # FIXME: This is not working, because output is wrapped and name is splitted
    # for f in all_valid_files:
    #    assert f.name in result.stderr
    assert result.stderr.count(": OK") == len(all_valid_files)


def test_check_no_args_invalid_multiple(runner: CliRunner, all_invalid_files: list[Path]) -> None:
    """Test check with no args and multiple invalid files."""
    result = runner.invoke(app, ["check"])
    assert f"Found {len(all_invalid_files)} Corsair file" in result.stderr
    assert result.exit_code != 0
    # FIXME: This is not working, because output is wrapped and name is splitted
    # for f in all_invalid_files:
    #    assert f.name in result.stderr
    assert result.stderr.count(": FAIL") == len(all_invalid_files)


def test_check_no_args_mixed(runner: CliRunner, valid_build_file: Path, invalid_build_file: Path) -> None:  # noqa: ARG001
    """Test check with no args and mixed valid and invalid files."""
    result = runner.invoke(app, ["check"])
    assert "Found 2 Corsair file" in result.stderr
    assert result.exit_code != 0
    # FIXME: This is not working, because output is wrapped and name is splitted
    # for f in all_invalid_files:
    #    assert f.name in result.stderr
    assert result.stderr.count(": FAIL") == 1
    assert result.stderr.count(": OK") == 1


def test_check_args_valid_build(runner: CliRunner, valid_build_file: Path) -> None:
    """Test check with args and a valid build file."""
    result = runner.invoke(app, ["check", str(valid_build_file)])
    assert "Using provided 1 input file" in result.stderr
    assert result.exit_code == 0
    assert result.stderr.count(": OK") == 1


def test_check_args_invalid_build(runner: CliRunner, invalid_build_file: Path) -> None:
    """Test check with args and an invalid build file."""
    result = runner.invoke(app, ["check", str(invalid_build_file)])
    assert "Using provided 1 input file" in result.stderr
    assert result.exit_code != 0
    assert isinstance(result.exception, RuntimeError)
    assert result.stderr.count(": FAIL") == 1


def test_check_args_valid_map(runner: CliRunner, valid_map_file: Path) -> None:
    """Test check with args and a valid map file."""
    result = runner.invoke(app, ["check", str(valid_map_file)])
    assert "Using provided 1 input file" in result.stderr
    assert result.exit_code == 0
    assert result.stderr.count(": OK") == 1


def test_check_args_invalid_map(runner: CliRunner, invalid_map_file: Path) -> None:
    """Test check with args and an invalid map file."""
    result = runner.invoke(app, ["check", str(invalid_map_file)])
    assert "Using provided 1 input file" in result.stderr
    assert result.exit_code != 0
    assert isinstance(result.exception, RuntimeError)
    assert result.stderr.count(": FAIL") == 1


def test_check_args_valid_multiple(runner: CliRunner, all_valid_files: list[Path]) -> None:
    """Test check with args and multiple valid files."""
    args = ["check"] + [str(f) for f in all_valid_files]
    result = runner.invoke(app, args)
    assert f"Using provided {len(all_valid_files)} input file" in result.stderr
    assert result.exit_code == 0
    assert result.stderr.count(": OK") == len(all_valid_files)


def test_check_args_invalid_multiple(runner: CliRunner, all_invalid_files: list[Path]) -> None:
    """Test check with args and multiple invalid files."""
    args = ["check"] + [str(f) for f in all_invalid_files]
    result = runner.invoke(app, args)
    assert f"Using provided {len(all_invalid_files)} input file" in result.stderr
    assert result.exit_code != 0
    assert result.stderr.count(": FAIL") == len(all_invalid_files)


def test_check_args_mixed(runner: CliRunner, valid_build_file: Path, invalid_build_file: Path) -> None:
    """Test check with args and mixed valid and invalid files."""
    args = ["check", str(valid_build_file), str(invalid_build_file)]
    result = runner.invoke(app, args)
    assert "Using provided 2 input file" in result.stderr
    assert result.exit_code != 0
    assert result.stderr.count(": FAIL") == 1
    assert result.stderr.count(": OK") == 1


def test_check_args_non_existent_file(runner: CliRunner) -> None:
    """Test check with a non-existent file path argument."""
    result = runner.invoke(app, ["check", "non_existent_file.toml"])
    assert result.exit_code != 0
    assert isinstance(result.exception, FileNotFoundError)
    assert "Input file not found: 'non_existent_file.toml'" in str(result.exception)


def test_check_args_directory(runner: CliRunner, tmp_path: Path) -> None:
    """Test check with a directory path argument."""
    (tmp_path / "some_dir").mkdir()
    result = runner.invoke(app, ["check", str(tmp_path / "some_dir")])
    assert result.exit_code != 0
    assert isinstance(result.exception, IsADirectoryError)
    assert "Input path is a directory" in str(result.exception)


def test_check_args_unsupported_extension(runner: CliRunner, tmp_path: Path) -> None:
    """Test check with an unsupported file extension."""
    p = tmp_path / "file.txt"
    p.touch()
    result = runner.invoke(app, ["check", str(p)])
    assert result.exit_code != 0
    assert isinstance(result.exception, RuntimeError)
    assert "Unknown or unsupported extension" in result.stderr
