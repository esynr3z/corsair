"""Available targets to build.

These data models act as a data validation frontend for options for output generators.
"""

from __future__ import annotations

from typing import Annotated, Literal, Union

from pydantic import BaseModel, ConfigDict, Field, StringConstraints

_VAR_NAME_RE = r"^[A-Za-z_][A-Za-z0-9_]*$"


class BaseTarget(BaseModel):
    """Base target to generate."""

    model_config = ConfigDict(
        extra="allow",
        arbitrary_types_allowed=True,
        use_attribute_docstrings=True,
    )


class CustomTarget(BaseTarget):
    """Custom target that uses custom generator class to produce output."""

    kind: Literal["custom"]
    """Target kind discriminator."""

    generator: Annotated[
        str,
        StringConstraints(
            strip_whitespace=True,
            pattern=r"^.*\.py::\w+$",
        ),
    ] = Field(examples=["bar.py::BarGenerator"])
    """Path to a custom generator class to be used."""


class MapVerilogTarget(BaseTarget):
    """Target to create Verilog file for a register map."""

    kind: Literal["map_verilog"]
    """Target kind discriminator."""


class MapVhdlTarget(BaseTarget):
    """Target to create VHDL file for a register map."""

    kind: Literal["map_vhdl"]
    """Target kind discriminator."""


class MapVerilogHeaderTarget(BaseTarget):
    """Target to create Verilog header file for a register map."""

    kind: Literal["map_verilog_header"]
    """Target kind discriminator."""

    prefix: Annotated[
        str,
        StringConstraints(
            strip_whitespace=True,
            to_lower=True,
            pattern=_VAR_NAME_RE,
        ),
    ] = "csr"
    """Prefix for all defines. Case does not matter."""


class MapCHeaderTarget(BaseTarget):
    """Target to create C header file for a register map."""

    kind: Literal["map_c_header"]
    """Target kind discriminator."""

    prefix: Annotated[
        str,
        StringConstraints(
            strip_whitespace=True,
            to_lower=True,
            pattern=_VAR_NAME_RE,
        ),
    ] = "csr"
    """Prefix for all defines. Case does not matter."""


class MapSvPackageTarget(BaseTarget):
    """Target to create SystemVerilog package file for a register map."""

    kind: Literal["map_sv_package"]
    """Target kind discriminator."""

    prefix: Annotated[
        str,
        StringConstraints(
            strip_whitespace=True,
            to_lower=True,
            pattern=_VAR_NAME_RE,
        ),
    ] = "csr"
    """Prefix for all parameters. Case does not matter."""


class MapMarkdownTarget(BaseTarget):
    """Target to create a Markdown file for a register map."""

    kind: Literal["map_markdown"]
    """Target kind discriminator."""

    title: str = "Register map"
    """Document title."""

    print_images: bool = True
    """Enable generating images for bit fields."""

    print_conventions: bool = True
    """Enable generation of access modes table."""


AnyTarget = Annotated[
    Union[
        CustomTarget,
        MapVerilogTarget,
        MapVhdlTarget,
        MapVerilogHeaderTarget,
        MapCHeaderTarget,
        MapSvPackageTarget,
        MapMarkdownTarget,
    ],
    Field(discriminator="kind"),
]
"""Any known target."""
