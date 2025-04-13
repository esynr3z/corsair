"""Environment for internal Jinja2 templates."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any

from jinja2 import Environment, FileSystemLoader, StrictUndefined

from corsair._version import VERSION

if TYPE_CHECKING:
    from typing_extensions import Self


class TemplateEnvironment(Environment):
    """Singleton environment for managing Jinja2 templates."""

    _instance: Self | None = None

    def __new__(cls, *args: Any, **kwargs: Any) -> Self:  # noqa: ARG003
        """Create a new template environment."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, searchpaths: list[Path] | None = None) -> None:
        """Initialize the template environment."""
        if not searchpaths:
            searchpaths = []
        searchpaths.append(Path(__file__).parent)

        super().__init__(
            loader=FileSystemLoader(searchpath=searchpaths),
            trim_blocks=True,
            lstrip_blocks=True,
            undefined=StrictUndefined,  # to throw exception on any undefined variable within template
        )

        self.globals.update(
            version=VERSION,  # version should be available in all templates
            zip=zip,  # add zip function
        )
