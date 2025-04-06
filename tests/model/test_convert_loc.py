"""Tests conversion of schema location to path location."""

from __future__ import annotations

import pytest

import corsair as csr

# All tests below can be used in smoke testing
pytestmark = pytest.mark.smoke


# Fixture data containing test cases
# Each tuple: pytest.param(data, schema_loc, golden_path_loc, id=test_id)
TEST_CASES = [
    # Test when error is in the map field.
    pytest.param(
        {
            "name": "default_map",
            "doc": None,
        },
        ("doc",),
        ("default_map", "doc"),
        id="test_map_field_error",
    ),
    # Test when error is the absence of the map field.
    pytest.param(
        {
            "name": "default_map",
        },
        ("doc",),
        ("default_map", "doc"),
        id="test_map_field_absent",
    ),
    # Test when error is the absence of the map name.
    pytest.param(
        {},
        ("name",),
        ("<unknown>", "name"),
        id="test_map_name_absent",
    ),
    # Test when error is the wrong name of the map.
    pytest.param(
        {
            "name": None,
        },
        ("name",),
        ("<unknown>", "name"),
        id="test_map_name_wrong",
    ),
    # Test when error is in the register field.
    pytest.param(
        {
            "name": "default_map",
            "items": [
                {
                    "name": "reg_a",
                    "offset": -1,
                }
            ],
        },
        ("items", 0, "register", "offset"),
        ("default_map", "reg_a", "offset"),
        id="test_register_field_error",
    ),
    # Test when error is the absence of the register field.
    pytest.param(
        {
            "name": "default_map",
            "items": [
                {
                    "name": "reg_a",
                }
            ],
        },
        ("items", 0, "register", "offset"),
        ("default_map", "reg_a", "offset"),
        id="test_register_field_absent",
    ),
    # Test when error is the absence of the register name.
    pytest.param(
        {"name": "default_map", "items": [{}]},
        ("items", 0, "register", "name"),
        ("default_map", "<unknown>", "name"),
        id="test_register_name_absent",
    ),
    # Test when error is the wrong name of the register.
    pytest.param(
        {
            "name": "default_map",
            "items": [
                {
                    "name": None,
                }
            ],
        },
        ("items", 0, "register", "name"),
        ("default_map", "<unknown>", "name"),
        id="test_register_name_wrong",
    ),
    # Test when error is in the field field.
    pytest.param(
        {
            "name": "default_map",
            "items": [
                {
                    "name": "reg_a",
                    "fields": [
                        {
                            "name": "field_a",
                            "offset": -1,
                        }
                    ],
                }
            ],
        },
        ("items", 0, "register", "fields", 0, "offset"),
        ("default_map", "reg_a", "field_a", "offset"),
        id="test_field_field_error",
    ),
    # Test when error is the absence of the field field.
    pytest.param(
        {
            "name": "default_map",
            "items": [
                {
                    "name": "reg_a",
                    "fields": [
                        {
                            "name": "field_a",
                        }
                    ],
                }
            ],
        },
        ("items", 0, "register", "fields", 0, "offset"),
        ("default_map", "reg_a", "field_a", "offset"),
        id="test_field_field_absent",
    ),
    # Test when error is the absence of the field name.
    pytest.param(
        {"name": "default_map", "items": [{"name": "reg_a", "fields": [{}]}]},
        ("items", 0, "register", "fields", 0, "name"),
        ("default_map", "reg_a", "<unknown>", "name"),
        id="test_field_name_absent",
    ),
    # Test when error is the wrong name of the field.
    pytest.param(
        {
            "name": "default_map",
            "items": [
                {
                    "name": "reg_a",
                    "fields": [
                        {
                            "name": None,
                        }
                    ],
                }
            ],
        },
        ("items", 0, "register", "fields", 0, "name"),
        ("default_map", "reg_a", "<unknown>", "name"),
        id="test_field_name_wrong",
    ),
    # Test when error is the wrong name of the enum.
    pytest.param(
        {
            "name": "default_map",
            "items": [
                {
                    "name": "reg_a",
                    "fields": [
                        {
                            "name": "field_a",
                            "enum": {"name": None},
                        }
                    ],
                }
            ],
        },
        ("items", 0, "register", "fields", 0, "enum", "name"),
        ("default_map", "reg_a", "field_a", "<unknown>", "name"),
        id="test_enum_name_wrong",
    ),
    # Test when error is the absence of the enum name.
    pytest.param(
        {
            "name": "default_map",
            "items": [
                {
                    "name": "reg_a",
                    "fields": [
                        {
                            "name": "field_a",
                            "enum": {},
                        }
                    ],
                }
            ],
        },
        ("items", 0, "register", "fields", 0, "enum", "name"),
        ("default_map", "reg_a", "field_a", "<unknown>", "name"),
        id="test_enum_name_absent",
    ),
    # Test when error is in the enum field.
    pytest.param(
        {
            "name": "default_map",
            "items": [
                {
                    "name": "reg_a",
                    "fields": [
                        {
                            "name": "field_a",
                            "enum": {"name": "enum_a", "value": -1},
                        }
                    ],
                }
            ],
        },
        ("items", 0, "register", "fields", 0, "enum", "value"),
        ("default_map", "reg_a", "field_a", "enum_a", "value"),
        id="test_enum_field_error",
    ),
    # Test when error is the validation failure of the enum.
    pytest.param(
        {
            "name": "default_map",
            "items": [
                {
                    "name": "reg_a",
                    "fields": [
                        {
                            "name": "field_a",
                            "enum": {
                                "name": "enum_a",
                                "value": -1,
                            },
                        }
                    ],
                }
            ],
        },
        ("items", 0, "register", "fields", 0, "enum"),
        ("default_map", "reg_a", "field_a", "enum_a"),
        id="test_enum_validation_fail",
    ),
    # Test when error is the validation failure of the field.
    pytest.param(
        {
            "name": "default_map",
            "items": [
                {
                    "name": "reg_a",
                    "fields": [
                        {
                            "name": "field_a",
                        }
                    ],
                }
            ],
        },
        ("items", 0, "register", "fields", 0),
        ("default_map", "reg_a", "field_a"),
        id="test_field_validation_fail",
    ),
    # Test when error is the validation failure of the fields.
    pytest.param(
        {
            "name": "default_map",
            "items": [{"name": "reg_a", "fields": "wrong"}],
        },
        ("items", 0, "register", "fields"),
        ("default_map", "reg_a", "fields"),
        id="test_fields_validation_fail",
    ),
    # Test when error is the validation failure of the register.
    pytest.param(
        {
            "name": "default_map",
            "items": [
                {
                    "name": "reg_a",
                }
            ],
        },
        ("items", 0, "register"),
        ("default_map", "reg_a"),
        id="test_register_validation_fail",
    ),
    # Test when error is the validation failure of the register without tag.
    pytest.param(
        {
            "name": "default_map",
            "items": [
                {
                    "name": "reg_a",
                }
            ],
        },
        ("items", 0),
        ("default_map", "reg_a"),
        id="test_register_validation_fail_no_tag",
    ),
]


@pytest.mark.parametrize(
    ("data", "schema_loc", "golden_path_loc"),
    TEST_CASES,
)
def test_conversion(
    data: dict,
    schema_loc: tuple[str | int, ...],
    golden_path_loc: tuple[str, ...],
) -> None:
    """Test conversion of schema location to path location."""
    tested_path_loc = csr.convert_schema_loc_to_path_loc(schema_loc, data)
    assert golden_path_loc == tested_path_loc
