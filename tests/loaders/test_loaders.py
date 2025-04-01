"""Tests for register map loaders based on collection of YAML files."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pydantic
import pytest
import yaml
from pydantic import ValidationError  # noqa: F401

import corsair as csr


@pydantic.dataclasses.dataclass
class RegisterMapTestParams:
    """Test parameters parsed from the YAML register map file."""

    doc: str | None = None
    """Description of the test."""

    exception: type[Exception] | None = None
    """Type of exception expected in the test."""

    msg_match: str | None = None
    """Regular expression pattern to match against the exception message."""

    @pydantic.field_validator("exception", mode="before")
    @classmethod
    def validate_exception(cls, value: Any) -> Any:
        """Convert exception name string to actual exception type."""
        if value is None:
            return None
        if isinstance(value, type) and issubclass(value, Exception):
            return value
        if isinstance(value, str):
            # Look up the exception in the built-in exceptions
            exception = globals().get(value) or __builtins__.get(value)
            if exception is not None and isinstance(exception, type) and issubclass(exception, Exception):
                return exception
            raise ValueError(f"Unknown exception type: {value}")
        raise ValueError(f"Invalid exception type: {value}")

    @classmethod
    def from_file(cls, file_path: Path) -> RegisterMapTestParams:
        """Parse test metadata from the YAML register map file."""
        header_lines = []
        with file_path.open("r", encoding="utf-8") as f:
            for line in f:
                if line.strip() == "---":
                    break
                header_lines.append(line)

        cleaned_lines: list[str] = [line.lstrip("#").strip() for line in header_lines if line.startswith("#")]
        header = "\n".join(cleaned_lines)

        try:
            params = yaml.safe_load(header)
            return cls(**params)
        except yaml.YAMLError as e:
            raise ValueError(f"Error parsing YAML header in {file_path}: {e}") from e


def get_yaml_files() -> list[Path]:
    """Get all YAML files in the tests/data directory."""
    directory = Path(__file__).parent / "data"
    return [p for p in directory.glob("*") if p.suffix in (".yaml", ".yml")]


@pytest.mark.parametrize("yaml_file", get_yaml_files(), ids=lambda p: p.stem)
def test_serialized_yaml(yaml_file: Path) -> None:
    """Test that the `SerializedLoader` can load register map from YAML files."""
    # Extract expected test parameters from the YAML file header.
    test_params = RegisterMapTestParams.from_file(yaml_file)

    # Load the YAML file using the `SerializedLoader`.
    loader_cfg = csr.SerializedLoader.Config(kind="yaml", mapfile=yaml_file)

    if test_params.exception is None:
        _ = csr.SerializedLoader(config=loader_cfg)()
    else:
        try:
            with pytest.raises(test_params.exception, match=test_params.msg_match):
                _ = csr.SerializedLoader(config=loader_cfg)()
        except Exception as e:
            raise AssertionError(f"{test_params.doc}\n{e}") from e
