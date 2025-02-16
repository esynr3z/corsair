"""Utility functions for tests."""

from __future__ import annotations

from typing import Any

import corsair as csr


def build_enum_member(**kwargs: Any) -> csr.EnumMember:
    """Create default enum member."""
    defaults = {
        "name": "ok",
        "doc": "Indicates status is OK",
        "value": 0,
    }
    defaults.update(kwargs)
    return csr.EnumMember(**defaults)


def build_enum(members: tuple[csr.EnumMember, ...], **kwargs: Any) -> csr.Enum:
    """Create default enum member."""
    defaults = {
        "name": "enum",
        "doc": "Some enumeration",
        "members": members,
    }
    defaults.update(kwargs)
    return csr.Enum(**defaults)


def build_field(**kwargs: Any) -> csr.Field:
    """Return a default Field instance with optional overrides."""
    defaults = {
        "name": "field_name",
        "doc": "A brief description.\n\nA detailed description of the field.",
        "reset": 0,
        "width": 8,
        "offset": 0,
        "access": csr.AccessMode.RW,
        "hardware": csr.HardwareMode.NA,
        "enum": None,
    }
    defaults.update(kwargs)
    return csr.Field(**defaults)


def build_register(**kwargs: Any) -> csr.Register:
    """Return a default Register instance with optional overrides."""
    defaults = {
        "name": "test_register",
        "doc": "Test register.",
        "offset": 0,
        "fields": (build_field(),),
    }
    defaults.update(kwargs)
    return csr.Register(**defaults)


def build_map(**kwargs: Any) -> csr.Map:
    """Return a default Map instance with optional overrides."""
    defaults = {
        "name": "test_map",
        "doc": "Test map.",
        "offset": 0,
        "address_width": 12,
        "register_width": 32,
        "items": (build_register(),),
    }
    defaults.update(kwargs)
    return csr.Map(**defaults)


def build_memory(**kwargs: Any) -> csr.Memory:
    """Return a default Memory instance with optional overrides."""
    defaults = {
        "name": "test_memory",
        "doc": "Test memory.",
        "offset": 0,
        "address_width": 12,
        "data_width": 32,
        "style": csr.MemoryStyle.INTERNAL_RW,
        "initial_values": (),
    }
    defaults.update(kwargs)
    return csr.Memory(**defaults)
