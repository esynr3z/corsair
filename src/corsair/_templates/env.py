"""Environment for internal Jinja2 templates."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any

from jinja2 import Environment, FileSystemLoader, StrictUndefined, TemplateNotFound

from corsair._version import VERSION

if TYPE_CHECKING:
    from collections.abc import Callable

    from typing_extensions import Self


class _EnhancedFileSystemLoader(FileSystemLoader):
    """Custom Jinja2 FileSystemLoader that supports both relative and absolute paths."""

    def __init__(self, searchpath: list[Path], **kwargs: Any) -> None:
        super().__init__(searchpath=searchpath, **kwargs)

    def get_source(
        self,
        environment: Environment,
        template: str,
    ) -> tuple[str, str, Callable[[], bool]]:
        """Get the template source, filename and reload helper for a template.

        Checks for absolute paths first, otherwise delegates to the parent FileSystemLoader.
        """
        template_path = Path(template)
        if template_path.is_absolute():
            if not template_path.is_file():
                raise TemplateNotFound(template)

            mtime = template_path.stat().st_mtime
            with template_path.open("r", encoding="utf-8") as f:
                source = f.read()

            # Return the source, filename (absolute path), and a mtime check function
            return source, str(template_path), lambda: template_path.stat().st_mtime == mtime

        # If it's not an absolute path, delegate to the parent class method
        return super().get_source(environment, template)


class TemplateEnvironment(Environment):
    """Singleton environment for managing Jinja2 templates."""

    _instance: Self | None = None

    def __new__(cls, *args: Any, **kwargs: Any) -> Self:  # noqa: ARG003
        """Create a new template environment."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, searchpath: list[Path] | None = None) -> None:
        """Initialize the template environment."""
        if not searchpath:
            searchpath = []

        # Always include the directory containing the built-in templates
        searchpath.append(Path(__file__).parent)

        super().__init__(
            loader=_EnhancedFileSystemLoader(searchpath=searchpath),
            trim_blocks=True,
            lstrip_blocks=True,
            undefined=StrictUndefined,  # to throw exception on any undefined variable within template
        )

        self.globals.update(
            version=VERSION,  # version should be available in all templates
            zip=zip,  # add zip function
        )
