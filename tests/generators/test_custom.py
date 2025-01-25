"""Tests for custom generators."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

import corsair as csr

if TYPE_CHECKING:
    from pathlib import Path


def test_config_init() -> None:
    """Test basic initialization of CustomGeneratorConfig."""
    config = csr.CustomGeneratorConfig(generator="test.py::TestGenerator")
    assert config.kind == "custom"
    assert config.generator == "test.py::TestGenerator"
    assert config.label == "custom"


def test_config_label_override() -> None:
    """Test that label can be overridden."""
    config = csr.CustomGeneratorConfig(generator="test.py::TestGenerator", label="custom_label")
    assert config.label == "custom_label"


def test_config_cls_loading(tmp_path: Path) -> None:
    """Test loading of generator class from file."""
    # Create a temporary test generator file
    test_file = tmp_path / "test_gen.py"
    test_file.write_text(
        """
from corsair import Generator

class TestGenerator(Generator):
    def __call__(self, output_dir, dry_run=False):
        pass

    @classmethod
    def get_config_cls(cls):
        pass
"""
    )

    config = csr.CustomGeneratorConfig(generator=f"{test_file}::TestGenerator")
    generator_cls = config.generator_cls
    assert generator_cls.__name__ == "TestGenerator"
    assert issubclass(generator_cls, csr.Generator)


def test_config_loading_missing_file() -> None:
    """Test error when loading generator from missing file."""
    config = csr.CustomGeneratorConfig(generator="missing.py::TestGenerator")
    with pytest.raises(FileNotFoundError, match="No such file or directory"):
        _ = config.generator_cls


def test_config_loading_missing_class(tmp_path: Path) -> None:
    """Test error when loading missing generator class."""
    test_file = tmp_path / "test_gen.py"
    test_file.write_text("")
    config = csr.CustomGeneratorConfig(generator=f"{test_file}::MissingGenerator")
    with pytest.raises(ImportError, match="'MissingGenerator' not found"):
        _ = config.generator_cls


def test_config_loading_wrong_type(tmp_path: Path) -> None:
    """Test error when loading class that is not a Generator."""
    test_file = tmp_path / "test_gen.py"
    test_file.write_text(
        """
class NotAGenerator:
    pass
"""
    )
    config = csr.CustomGeneratorConfig(generator=f"{test_file}::NotAGenerator")
    with pytest.raises(TypeError, match="must be a subclass of 'Generator'"):
        _ = config.generator_cls
