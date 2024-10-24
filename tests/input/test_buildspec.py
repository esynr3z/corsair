"""Tests corsair build specification."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from corsair import (
    BuildSpecification,
    GlobalConfig,
    MapMarkdownTarget,
    MapVerilogTarget,
)

# All tests below can be used in smoke testing
pytestmark = pytest.mark.smoke


def test_valid_buildspec() -> None:
    """Test that a valid BuildSpecification can be created with proper config and targets."""
    config_data = {"regmap": Path("path/to/regmap"), "data_width": 32}
    config = GlobalConfig(**config_data)

    targets_data = {
        "verilog": {"kind": "map_verilog"},
        "markdown": {"kind": "map_markdown", "title": "My Register Map"},
    }

    build_spec = BuildSpecification.model_validate({"config": config_data, "targets": targets_data})
    assert build_spec.config == config
    assert "verilog" in build_spec.targets
    assert isinstance(build_spec.targets["verilog"], MapVerilogTarget)
    assert isinstance(build_spec.targets["markdown"], MapMarkdownTarget)


def test_invalid_target_in_buildspec() -> None:
    """Test that BuildSpecification raises ValidationError for invalid targets."""
    config_data = {"regmap": Path("path/to/regmap"), "data_width": 32}
    config = GlobalConfig(**config_data)

    targets_data = {"invalid_target": {"kind": "invalid_kind"}}

    with pytest.raises(ValidationError):
        BuildSpecification.model_validate({"config": config, "targets": targets_data})


def test_buildspec_from_toml_file(tmp_path: Path) -> None:
    """Test that BuildSpecification can be loaded from a TOML file."""
    # Prepare TOML content
    toml_content = """
    [config]
    regmap = "path/to/regmap"
    data_width = 32

    [targets.verilog]
    kind = "map_verilog"

    [targets.markdown]
    kind = "map_markdown"
    title = "My Register Map"
    """

    # Write the TOML content to a temporary file
    toml_file = tmp_path / "csrbuild.toml"
    toml_file.write_text(toml_content)

    # Load the BuildSpecification from the TOML file
    build_spec = BuildSpecification.from_toml_file(toml_file)

    assert str(build_spec.config.regmap) == "path/to/regmap"
    assert build_spec.config.data_width == 32
    assert "verilog" in build_spec.targets
    assert build_spec.targets["verilog"].kind == "map_verilog"


def test_buildspec_to_json_schema_file(tmp_path: Path) -> None:
    """Test that BuildSpecification can output its JSON schema to a file."""
    # Define the path to the temporary JSON schema file
    json_schema_file = tmp_path / "csrbuild.schema.json"

    # Generate the JSON schema file
    BuildSpecification.to_json_schema_file(json_schema_file)

    # Read the generated JSON schema file
    assert json_schema_file.exists()
    schema_content = json_schema_file.read_text()

    # Basic assertion to check that the content is not empty
    assert len(schema_content) > 0

    # Load and validate the JSON content
    schema = json.loads(schema_content)
    assert "title" in schema
    assert schema["title"] == "BuildSpecification"
