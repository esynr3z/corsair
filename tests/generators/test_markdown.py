"""Tests for the Markdown generator."""

from __future__ import annotations

from pathlib import Path

import pytest

import corsair as csr


@pytest.fixture
def simple_regmap() -> csr.Map:
    """Create a simple register map for testing."""
    field1 = csr.Field(
        name="FIELD1",
        offset=0,
        width=8,
        access=csr.AccessMode.RW,
        hardware=csr.HardwareMode.NA,
        doc="Field 1",
        reset=0xAA,
    )
    field2 = csr.Field(
        name="FIELD2",
        offset=8,
        width=16,
        access=csr.AccessMode.RO,
        hardware=csr.HardwareMode.NA,
        doc="Field 2",
        reset=None,
    )
    reg1 = csr.Register(
        name="REG1",
        offset=0,
        doc="Register 1\n\nThis is a description of register 1",
        fields=(field1, field2),
    )

    field3 = csr.Field(
        name="FIELD3",
        offset=0,
        width=1,
        access=csr.AccessMode.WO,
        hardware=csr.HardwareMode.NA,
        doc="Field 3",
        reset=0,
        enum=csr.Enum(
            name="mode",
            doc="Mode",
            members=(
                csr.EnumMember(name="MODE1", value=0, doc="Mode 1\n\nThis is a description of mode 1"),
                csr.EnumMember(name="MODE2", value=1, doc="Mode 2\n\nThis is a description of mode 2"),
            ),
        ),
    )
    reg2 = csr.Register(name="REG2", offset=4, doc="Register 2", fields=(field3,))

    return csr.Map(
        name="test_map",
        offset=0,
        address_width=32,
        register_width=32,
        doc="Test map",
        items=(reg1, reg2),
    )


@pytest.fixture
def custom_template(tmp_path: Path) -> Path:
    """Create a custom template file directly in tmp_path and return its absolute path."""
    template_name = "custom_template_fixture.md.j2"
    template_content = (
        """"" \
# Custom Template Fixture Test

Registers:
{% for item in regmap.items %}
- {{ item.name }}
{% endfor %}

{% if cfg.extra['my_param'] is defined %}
Custom Param: {{ cfg.extra['my_param'] }}
{% endif %}
"""
        ""
    )  # Raw string literal to handle backslashes correctly
    template_file = tmp_path / template_name
    template_file.write_text(template_content)
    return template_file.resolve()  # Return absolute path


def test_default_generation(tmp_path: Path, simple_regmap: csr.Map) -> None:
    """Test default Markdown generation."""
    config = csr.MarkdownGenerator.Config()
    gen = csr.MarkdownGenerator(
        label="test_md_gen_default", register_map=simple_regmap, config=config, output_dir=tmp_path
    )
    generated_files = set(gen())

    expected_file = tmp_path / "regmap.md"
    expected_files = {expected_file}

    assert generated_files == expected_files
    assert expected_file.is_file()
    assert not (tmp_path / "img").exists()


def test_custom_file_name(tmp_path: Path, simple_regmap: csr.Map) -> None:
    """Test that file_name config affects the output file name."""
    custom_name = "custom_map.md"
    config = csr.MarkdownGenerator.Config(file_name=custom_name)
    gen = csr.MarkdownGenerator(
        label="test_md_gen_fname", register_map=simple_regmap, config=config, output_dir=tmp_path
    )
    generated_files = set(gen())

    expected_file = tmp_path / custom_name
    expected_files = {expected_file}

    assert generated_files == expected_files
    assert expected_file.is_file()


def test_title_in_output(tmp_path: Path, simple_regmap: csr.Map) -> None:
    """Test that the title config appears in the output file."""
    custom_title = "My Custom Register Map"
    config = csr.MarkdownGenerator.Config(title=custom_title)
    gen = csr.MarkdownGenerator(
        label="test_md_gen_title", register_map=simple_regmap, config=config, output_dir=tmp_path
    )
    generated_files = list(gen())

    assert len(generated_files) == 1
    output_file = generated_files[0]
    assert output_file.is_file()

    content = output_file.read_text()
    assert f"# {custom_title}" in content


def test_show_conventions_true(tmp_path: Path, simple_regmap: csr.Map) -> None:
    """Test that conventions are printed when show_conventions is True."""
    config = csr.MarkdownGenerator.Config(show_conventions=True)
    gen = csr.MarkdownGenerator(
        label="test_md_gen_conv_true", register_map=simple_regmap, config=config, output_dir=tmp_path
    )
    generated_files = list(gen())
    output_file = generated_files[0]
    content = output_file.read_text()
    assert "## Conventions" in content
    assert "| Read and Write 1 to Clear" in content


def test_show_conventions_false(tmp_path: Path, simple_regmap: csr.Map) -> None:
    """Test that conventions are not printed when show_conventions is False."""
    config = csr.MarkdownGenerator.Config(show_conventions=False)
    gen = csr.MarkdownGenerator(
        label="test_md_gen_conv_false", register_map=simple_regmap, config=config, output_dir=tmp_path
    )
    generated_files = list(gen())
    output_file = generated_files[0]
    content = output_file.read_text()
    assert "## Conventions" not in content
    assert "| Read and Write 1 to Clear" not in content


def test_show_images_false(tmp_path: Path, simple_regmap: csr.Map) -> None:
    """Test that no image directory is created when show_images is False."""
    config = csr.MarkdownGenerator.Config(show_images=False)
    gen = csr.MarkdownGenerator(
        label="test_md_gen_img_false", register_map=simple_regmap, config=config, output_dir=tmp_path
    )
    generated_files = set(gen())

    expected_file = tmp_path / "regmap.md"
    expected_files = {expected_file}

    assert generated_files == expected_files
    assert not (tmp_path / config.image_dir).exists()


def test_show_images_true(tmp_path: Path, simple_regmap: csr.Map) -> None:
    """Test that image directory and SVG files are created when show_images is True."""
    image_dir_name = "register_images"
    config = csr.MarkdownGenerator.Config(
        show_images=True,
        image_dir=Path(image_dir_name),
    )
    gen = csr.MarkdownGenerator(
        label="test_md_gen_img_true", register_map=simple_regmap, config=config, output_dir=tmp_path
    )
    generated_files = set(gen())

    expected_md_file = tmp_path / "regmap.md"
    expected_img_dir = tmp_path / image_dir_name
    expected_svg_files = {
        expected_img_dir / "test_map_reg1.svg",
        expected_img_dir / "test_map_reg2.svg",
    }
    expected_files = {expected_md_file, *expected_svg_files}

    assert generated_files == expected_files
    assert expected_md_file.is_file()
    assert expected_img_dir.is_dir()
    assert {f for f in expected_img_dir.iterdir() if f.suffix == ".svg"} == expected_svg_files


def test_wavedrom_dump_json(tmp_path: Path, simple_regmap: csr.Map) -> None:
    """Test that JSON files are dumped alongside SVGs when wavedrom.dump_json is True."""
    image_dir_name = "register_data"
    wavedrom_config = csr.WaveDromGenerator.Config(dump_json=True)
    config = csr.MarkdownGenerator.Config(
        show_images=True,
        image_dir=Path(image_dir_name),
        wavedrom=wavedrom_config,
    )
    gen = csr.MarkdownGenerator(
        label="test_md_gen_wd_json", register_map=simple_regmap, config=config, output_dir=tmp_path
    )
    generated_files = set(gen())

    expected_md_file = tmp_path / "regmap.md"
    expected_data_dir = tmp_path / image_dir_name
    expected_svg_files = {
        expected_data_dir / "test_map_reg1.svg",
        expected_data_dir / "test_map_reg2.svg",
    }
    expected_json_files = {
        expected_data_dir / "test_map_reg1.json",
        expected_data_dir / "test_map_reg2.json",
    }
    expected_files = {expected_md_file, *expected_svg_files, *expected_json_files}

    assert generated_files == expected_files
    assert expected_md_file.is_file()
    assert expected_data_dir.is_dir()
    assert {f for f in expected_data_dir.iterdir() if f.suffix == ".svg"} == expected_svg_files
    assert {f for f in expected_data_dir.iterdir() if f.suffix == ".json"} == expected_json_files


def test_autogenerated_comment_present(tmp_path: Path, simple_regmap: csr.Map) -> None:
    """Test that the autogenerated comment is present in the output file."""
    config = csr.MarkdownGenerator.Config()
    gen = csr.MarkdownGenerator(
        label="test_md_gen_autogen_comment", register_map=simple_regmap, config=config, output_dir=tmp_path
    )
    generated_files = list(gen())

    assert len(generated_files) == 1
    output_file = generated_files[0]
    assert output_file.is_file()

    content = output_file.read_text()
    assert "[//]: # (DO NOT EDIT THIS AUTOGENERATED FILE. ALL CHANGES WILL BE LOST.)" in content


def test_show_disclaimer_true(tmp_path: Path, simple_regmap: csr.Map) -> None:
    """Test that disclaimer is printed when show_disclaimer is True."""
    config = csr.MarkdownGenerator.Config(show_disclaimer=True)
    gen = csr.MarkdownGenerator(
        label="test_md_gen_disclaimer_true", register_map=simple_regmap, config=config, output_dir=tmp_path
    )
    generated_files = list(gen())
    output_file = generated_files[0]
    content = output_file.read_text()
    assert "Generated by [Corsair]" in content


def test_show_disclaimer_false(tmp_path: Path, simple_regmap: csr.Map) -> None:
    """Test that disclaimer is not printed when show_disclaimer is False."""
    config = csr.MarkdownGenerator.Config(show_disclaimer=False)
    gen = csr.MarkdownGenerator(
        label="test_md_gen_disclaimer_false", register_map=simple_regmap, config=config, output_dir=tmp_path
    )
    generated_files = list(gen())
    output_file = generated_files[0]
    content = output_file.read_text()
    assert "Generated by [Corsair]" not in content


def test_show_hardware_mode_true(tmp_path: Path, simple_regmap: csr.Map) -> None:
    """Test that hardware mode conventions and column are present when show_hardware_mode is True."""
    config = csr.MarkdownGenerator.Config(show_hardware_mode=True)
    gen = csr.MarkdownGenerator(
        label="test_md_gen_hw_mode_true", register_map=simple_regmap, config=config, output_dir=tmp_path
    )
    generated_files = list(gen())
    output_file = generated_files[0]
    content = output_file.read_text()
    assert "## Conventions" in content  # Assuming conventions are shown by default or with hardware mode
    assert "| Hardware mode | Description |" in content
    assert "| Hardware |" in content  # Check for the column in the fields table


def test_show_hardware_mode_false(tmp_path: Path, simple_regmap: csr.Map) -> None:
    """Test that hardware mode conventions and column are absent when show_hardware_mode is False."""
    config = csr.MarkdownGenerator.Config(show_hardware_mode=False)
    gen = csr.MarkdownGenerator(
        label="test_md_gen_hw_mode_false", register_map=simple_regmap, config=config, output_dir=tmp_path
    )
    generated_files = list(gen())
    output_file = generated_files[0]
    content = output_file.read_text()
    # Assuming default of show_conventions=True, so "## Conventions" might still be there
    # We specifically check for the *hardware mode* conventions table
    assert "| Hardware mode | Description |" not in content
    assert "| Hardware |" not in content  # Check for the column in the fields table


def test_custom_template_and_extra_param(tmp_path: Path, simple_regmap: csr.Map, custom_template: Path) -> None:
    """Test generation with a custom template and extra config parameters."""
    template_file = custom_template

    custom_key = "my_param"
    custom_value = "hello_world"
    config = csr.MarkdownGenerator.Config(template_name=str(template_file), extra={custom_key: custom_value})

    gen = csr.MarkdownGenerator(
        label="test_md_gen_custom_tmpl",
        register_map=simple_regmap,
        config=config,
        output_dir=tmp_path,
    )
    generated_files = list(gen())

    # Check that the default file name is used if not specified
    expected_file = tmp_path / "regmap.md"
    assert generated_files == [expected_file]
    assert expected_file.is_file()

    # Check the content of the generated file
    content = expected_file.read_text()
    assert "# Custom Template Fixture Test" in content
    assert "Registers:" in content
    assert "- reg1" in content
    assert "- reg2" in content
    assert f"Custom Param: {custom_value}" in content


def test_custom_template_searchpath(tmp_path: Path, simple_regmap: csr.Map, custom_template: Path) -> None:
    """Test generation with a custom template specified via search path."""
    template_file = custom_template  # Fixture now returns the absolute path
    templates_dir = template_file.parent
    template_name = template_file.name

    # Configure the generator to use the custom template directory and name
    config = csr.MarkdownGenerator.Config(
        template_searchpaths=[templates_dir],
        template_name=template_name,
    )

    gen = csr.MarkdownGenerator(
        label="test_md_gen_searchpath",
        register_map=simple_regmap,
        config=config,
        output_dir=tmp_path,
    )

    # Running the generator should succeed without TemplateNotFound
    try:
        list(gen())
    except csr.GeneratorTemplateError as e:
        pytest.fail(f"Template generation failed: {e}")
