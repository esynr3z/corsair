"""Environment for internal Jinja2 templates."""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from jinja2 import Environment, PackageLoader, Template

if TYPE_CHECKING:
    from typing_extensions import Self


class TemplateKind(str, Enum):
    """Available Jinja2 templates."""

    REGMAP_VERILOG = "regmap.v.j2"
    REGMAP_VHDL = "regmap.vhd.j2"

    def __str__(self) -> str:
        """Convert enumeration member into string."""
        return self.value


class TemplateEnvironment(Environment):
    """Singleton environment for managing Jinja2 templates."""

    _instance: Self | None = None

    def __new__(cls) -> Self:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        super().__init__(loader=PackageLoader("corsair", "_templates"))

    def get_known_template(self, kind: TemplateKind) -> Template:
        """Get known template by its kind."""
        return self.get_template(str(kind))
