"""Test the 'build' command."""

from __future__ import annotations

import os
from pathlib import Path
from typing import TYPE_CHECKING

import pytest
from typer.testing import CliRunner

from corsair._app import app

if TYPE_CHECKING:
    from collections.abc import Generator


@pytest.fixture
def runner(tmp_path: Path) -> Generator[CliRunner, None, None]:
    """Fixture for invoking command-line interfaces."""
    original_cwd = Path.cwd()
    os.chdir(tmp_path)
    yield CliRunner(mix_stderr=False)
    os.chdir(original_cwd)


@pytest.fixture
def valid_map_file(tmp_path: Path) -> Path:
    """Fixture for a valid map file."""
    map_content = """
name: perhiph0
doc: Peripheral 0
offset: 0
address_width: 32
register_width: 32
items:
  - name: reg0
    doc: Register 0
    offset: 0
    fields:
      - name: field0
        doc: Field 0
        offset: 0
        width: 16
        access: ro
        reset: 1
        hardware: "n"
        enum: null
"""
    map_file = tmp_path / "csrmap.yaml"
    map_file.write_text(map_content)
    return map_file


@pytest.fixture
def valid_build_spec(tmp_path: Path, valid_map_file: Path) -> Path:
    """Fixture for a valid build spec."""
    spec_content = f"""
[loader]
kind = "yaml"
mapfile = "{valid_map_file.name}"

[[generators]]
label = "md0"
kind = "markdown"
file_name = "map.md"
print_images = true

[[generators]]
label = "md1"
kind = "markdown"
file_name = "map1.md"
print_images = false

[[generators]]
label = "wd"
kind = "wavedrom"
dump_json = true
render_svg = true
bits = 32
"""
    spec_file = tmp_path / "csrbuild.toml"
    spec_file.write_text(spec_content)
    return spec_file


def test_build_default_spec(runner: CliRunner, valid_build_spec: Path) -> None:  # noqa: ARG001
    """Test build uses default 'csrbuild.toml' when --spec is not provided."""
    result = runner.invoke(app, ["build"])
    assert result.exit_code == 0
    assert "Read build specification" in result.stderr
    assert Path("corsair-build").exists()
    # Check .gitignore is created
    assert Path("corsair-build/.gitignore").exists()
    assert Path("corsair-build/.gitignore").read_text() == "*\n"


def test_build_custom_spec(runner: CliRunner, valid_build_spec: Path) -> None:
    """Test build uses the user-provided build spec file."""
    result = runner.invoke(app, ["build", "--spec", str(valid_build_spec)])
    assert result.exit_code == 0
    assert "Read build specification" in result.stderr
    assert Path("corsair-build/md0/map.md").exists()


def test_build_all_targets_default(runner: CliRunner, valid_build_spec: Path) -> None:  # noqa: ARG001
    """Test build generates all targets when none are specified."""
    result = runner.invoke(app, ["build"])
    assert result.exit_code == 0
    assert "Targets to build: ['md0', 'md1', 'wd']" in result.stderr
    assert Path("corsair-build/md0/map.md").exists()
    assert Path("corsair-build/md1/map1.md").exists()
    assert Path("corsair-build/wd/perhiph0_reg0.svg").exists()


def test_build_single_target(runner: CliRunner, valid_build_spec: Path) -> None:  # noqa: ARG001
    """Test build generates only the specified single target."""
    result = runner.invoke(app, ["build", "md0"])
    assert result.exit_code == 0
    assert "Targets to build: ['md0']" in result.stderr
    assert Path("corsair-build/md0/map.md").exists()
    # Ensure other target wasn't built
    assert not Path("corsair-build/md1").exists()
    assert not Path("corsair-build/wd").exists()


def test_build_multiple_targets(runner: CliRunner, valid_build_spec: Path) -> None:  # noqa: ARG001
    """Test build generates only the specified multiple targets."""
    result = runner.invoke(app, ["build", "md0", "md1"])
    assert result.exit_code == 0
    assert "Targets to build: ['md0', 'md1']" in result.stderr
    assert Path("corsair-build/md0/map.md").exists()
    assert Path("corsair-build/md1/map1.md").exists()
    assert not Path("corsair-build/wd").exists()


def test_build_default_output_dir(runner: CliRunner, valid_build_spec: Path) -> None:  # noqa: ARG001
    """Test build uses the default output directory 'corsair-build'."""
    result = runner.invoke(app, ["build"])
    assert result.exit_code == 0
    assert Path("corsair-build").is_dir()
    assert Path("corsair-build/md0/map.md").exists()
    assert Path("corsair-build/md1/map1.md").exists()


def test_build_custom_output_dir(runner: CliRunner, valid_build_spec: Path, tmp_path: Path) -> None:  # noqa: ARG001
    """Test build uses the user-specified output directory."""
    custom_output = tmp_path / "custom_out"
    result = runner.invoke(app, ["build", "--output", str(custom_output)])
    assert result.exit_code == 0
    assert custom_output.is_dir()
    assert (custom_output / "md0/map.md").exists()
    assert (custom_output / "md1/map1.md").exists()
    # Ensure default wasn't created
    assert not Path("corsair-build").exists()


def test_build_incremental(runner: CliRunner, valid_build_spec: Path) -> None:  # noqa: ARG001
    """Test multiple build calls add targets to the same output directory."""
    # Build 'md' target first
    result1 = runner.invoke(app, ["build", "md0"])
    assert result1.exit_code == 0
    assert Path("corsair-build/md0/map.md").exists()
    assert not Path("corsair-build/md1").exists()

    # Build 'wd' target second
    result2 = runner.invoke(app, ["build", "md1"])
    assert result2.exit_code == 0
    assert Path("corsair-build/md0/map.md").exists()  # Still exists
    assert Path("corsair-build/md1/map1.md").exists()  # Now exists


def test_build_clean(runner: CliRunner, valid_build_spec: Path, tmp_path: Path) -> None:  # noqa: ARG001
    """Test the --clean option removes the output directory before building."""
    output_dir = tmp_path / "corsair-build"  # Explicitly use default for clarity

    # Run build once to create files
    result1 = runner.invoke(app, ["build", "md0"])
    assert result1.exit_code == 0
    assert (output_dir / "md0/map.md").exists()

    # Run build again with --clean and a different target
    result2 = runner.invoke(app, ["build", "wd", "--clean"])
    assert result2.exit_code == 0
    assert (output_dir / "wd/perhiph0_reg0.svg").exists()  # New target built
    assert not (output_dir / "md").exists()


def test_build_unknown_target(runner: CliRunner, valid_build_spec: Path) -> None:  # noqa: ARG001
    """Test build fails when an unknown target is specified."""
    result = runner.invoke(app, ["build", "unknown_target"])
    assert result.exit_code == 1
    assert "unknown_target" in result.stderr
    # Ensure known targets weren't built either
    assert not Path("corsair-build/md0").exists()
    assert not Path("corsair-build/md1").exists()
    assert not Path("corsair-build/wd").exists()


def test_build_output_is_cwd(runner: CliRunner, valid_build_spec: Path) -> None:  # noqa: ARG001
    """Test build fails if output directory is the current working directory."""
    result = runner.invoke(app, ["build", "--output", "."])
    assert result.exit_code == 1
    assert "In-source builds are not allowed" in result.stderr


def test_build_non_existent_spec(runner: CliRunner) -> None:
    """Test build fails if the specified build spec file does not exist."""
    result = runner.invoke(app, ["build", "--spec", "non_existent.csrbuild.toml"])
    assert result.exit_code == 1


def test_build_non_existent_map(runner: CliRunner, tmp_path: Path) -> None:
    """Test build fails if the map file specified in the build spec does not exist."""
    spec_content = """
[loader]
kind = "toml"
mapfile = "non_existent.csrmap.toml"

[[generators]]
label = "md"
kind = "markdown"
"""
    spec_file = tmp_path / "csrbuild.toml"
    spec_file.write_text(spec_content)

    result = runner.invoke(app, ["build"])
    assert result.exit_code == 1
    # The error originates from the loader trying to open the map file.
    assert result.exception is not None
    assert isinstance(result.exception, RuntimeError)  # Wrapper exception
    assert isinstance(result.exception.__cause__, FileNotFoundError)
    assert "non_existent.csrmap.toml" in str(result.exception.__cause__)
