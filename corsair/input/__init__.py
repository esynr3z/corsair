"""Data models, parsers and validators for all input files of corsair."""

from __future__ import annotations

from .buildspec import BuildSpecification
from .config import ForceNameCase, GlobalConfig, RegisterReset
from .target import (
    AnyTarget,
    BaseTarget,
    CustomTarget,
    MapCHeaderTarget,
    MapMarkdownTarget,
    MapSvPackageTarget,
    MapVerilogHeaderTarget,
    MapVerilogTarget,
    MapVhdlTarget,
)

__all__ = [
    # specification
    "BuildSpecification",
    # targets
    "AnyTarget",
    "BaseTarget",
    "CustomTarget",
    "MapVerilogTarget",
    "MapVhdlTarget",
    "MapSvPackageTarget",
    "MapVerilogHeaderTarget",
    "MapMarkdownTarget",
    "MapCHeaderTarget",
    # configuration
    "ForceNameCase",
    "RegisterReset",
    "GlobalConfig",
]
