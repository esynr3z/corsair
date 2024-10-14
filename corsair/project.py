"""Boilerpalte to create a simple example project for a user."""

from __future__ import annotations

from enum import Enum


class ProjectKind(str, Enum):
    """Project kind to generate."""

    JSON = "json"
    YAML = "yaml"
    TXT = "txt"
