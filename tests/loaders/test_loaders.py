"""Tests for register map loaders based on collection of YAML files."""

from __future__ import annotations

import importlib
import json
import re
from pathlib import Path
from typing import Any, Literal

import pydantic
import pytest
import yaml
from pydantic import ValidationError  # noqa: F401

import corsair as csr

HJSON_INSTALLED = importlib.util.find_spec("hjson") is not None  # type: ignore reportAttributeAccessIssue


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


def convert_yaml_to_json(yaml_path: Path, tmp_path: Path) -> Path:
    """Convert YAML file to JSON and save to a temporary file."""
    with yaml_path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    json_path = tmp_path / f"{yaml_path.stem}.json"
    with json_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    return json_path


def convert_yaml_to_hjson(yaml_path: Path, tmp_path: Path) -> Path:
    """Convert YAML file to HJSON and save to a temporary file."""
    import hjson

    with yaml_path.open("r", encoding="utf-8") as f:
        # Use load with comment support if needed, otherwise safe_load
        data = yaml.safe_load(f)
    hjson_path = tmp_path / f"{yaml_path.stem}.hjson"
    with hjson_path.open("w", encoding="utf-8") as f:
        hjson.dump(data, f)
    return hjson_path


# Combine yaml files and loader kinds for parametrization
LoaderKind = Literal["yaml", "json", "hjson"]
test_cases = [
    (yaml_file, loader_kind)
    for yaml_file in get_yaml_files()
    for loader_kind in ["yaml", "json", "hjson"]  # type: ignore[assignment]
]
test_ids = [f"{p[0].stem}.{p[1]}" for p in test_cases]


@pytest.mark.parametrize(("yaml_file", "loader_kind"), test_cases, ids=test_ids)
def test_serialized_yaml(yaml_file: Path, loader_kind: LoaderKind, tmp_path: Path) -> None:
    """Test that the `SerializedLoader` can load register maps from various file formats."""
    # Extract expected test parameters from the original YAML file header.
    test_params = RegisterMapTestParams.from_file(yaml_file)

    # Determine the mapfile path based on the loader kind
    if loader_kind == "json":
        mapfile = convert_yaml_to_json(yaml_file, tmp_path)
    elif loader_kind == "hjson":
        if not HJSON_INSTALLED:
            pytest.skip("hjson not installed")
        mapfile = convert_yaml_to_hjson(yaml_file, tmp_path)
    else:  # loader_kind == "yaml"
        mapfile = yaml_file

    # Load the file using the `SerializedLoader` with the specified kind and mapfile.
    loader_cfg = csr.SerializedLoader.Config(kind=loader_kind, mapfile=mapfile)

    if test_params.exception is None:
        # If no exception is expected, just run the loader.
        # Any unexpected exception will fail the test.
        _ = csr.SerializedLoader(config=loader_cfg)()
    else:
        # If an exception is expected, we specifically expect LoaderValidationError.
        # The original expected exception type and message match are now checked
        # against the stringified details within LoaderValidationError.
        with pytest.raises(csr.LoaderValidationError) as excinfo:
            _ = csr.SerializedLoader(config=loader_cfg)()

        # Check if the stringified error list contains the expected message pattern.
        # This makes the check more flexible than matching the entire exception string.
        if test_params.msg_match:
            assert any(
                re.search(test_params.msg_match, err_str) for err_str in excinfo.value.error_messages
            ), f"Expected pattern '{test_params.msg_match}' not found in loader errors: {excinfo.value.error_messages}"
