"""Base classes for all generators."""

from __future__ import annotations

import contextlib
import os
from abc import ABC, abstractmethod
from enum import Enum
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from collections.abc import Generator as TypeGenerator

    from corsair._model import Map

import jinja2
from pydantic import BaseModel, ConfigDict

from corsair._templates import TemplateEnvironment


@contextlib.contextmanager
def _change_workdir(path: Path) -> TypeGenerator[None, None, None]:
    """Change the working directory for the duration of the context."""
    old_cwd = Path.cwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(old_cwd)


class GeneratorTemplateError(Exception):
    """Raised when generator fails to render a template."""

    def __init__(self, generator: Generator, j2_error: jinja2.TemplateError) -> None:
        """Initialize the exception."""
        self.generator = generator
        self.j2_error = j2_error
        super().__init__(f"Generator '{generator.label}' failed to render template")

    def __str__(self) -> str:
        """Represent exception as a string."""
        err = f"{self.args[0]}\n"

        if isinstance(self.j2_error, jinja2.TemplateSyntaxError):
            err += "Syntax error within template"
            if self.j2_error.name:
                err += f" '{self.j2_error.name}'"
            if self.j2_error.filename:
                err += f" {self.j2_error.filename}:{self.j2_error.lineno}"
            if self.j2_error.message:
                err += f" {self.j2_error.message}"
            if self.j2_error.source:
                err += f"\n{self.j2_error.source.splitlines()[self.j2_error.lineno - 1]}"

        elif isinstance(self.j2_error, jinja2.UndefinedError):
            err += "Undefined variable within template"
            if self.j2_error.message:
                err += f": {self.j2_error.message}"

        return err


class GeneratorUnsupportedFeatureError(Exception):
    """Raised when generator encounters unsupported feature in the register map."""

    def __init__(self, generator: Generator, feature: str) -> None:
        """Initialize the exception."""
        self.generator = generator
        self.feature = feature

    def __str__(self) -> str:
        """Represent exception as a string."""
        err = f"Generator '{self.generator.label}' ({self.generator.config.get_kind()}) does not support feature: "
        err += self.feature
        return err


class GeneratorConfig(BaseModel, ABC):
    """Base configuration for a generator."""

    model_config = ConfigDict(
        extra="forbid",
        use_attribute_docstrings=True,
    )

    @property
    @abstractmethod
    def generator_cls(self) -> type[Generator]:
        """Related generator class."""

    @abstractmethod
    def get_kind(self) -> str:
        """Get the kind of the generator."""


class Generator(ABC):
    """Base class for all generators."""

    def __init__(
        self,
        label: str,
        register_map: Map,
        config: GeneratorConfig,
        output_dir: Path,
        template_searchpaths: list[Path] | None = None,
    ) -> None:
        """Initialize the generator."""
        self.label = label
        self.register_map = register_map
        self.config = config
        self.output_dir = output_dir.resolve()
        self.template_searchpaths = template_searchpaths

        if not isinstance(self.config, self.get_config_cls()):
            raise TypeError(
                f"Configuration instance is not of the expected type of "
                f"{self.__class__.__name__}.{self.get_config_cls().__name__}"
            )

    def __call__(self) -> TypeGenerator[Path, None, None]:
        """Generate all the outputs."""
        self._check_register_map()

        # Generation is isolated within the output directory
        self.output_dir.mkdir(parents=True, exist_ok=True)
        with _change_workdir(self.output_dir):
            try:
                yield from (p.resolve() for p in self._generate())
            except jinja2.TemplateError as e:
                raise GeneratorTemplateError(self, e) from e
            except Exception:
                raise

    def _render_to_text(self, template_name: str, context: dict[str, Any]) -> str:
        """Render text with Jinja2."""
        env = TemplateEnvironment(searchpaths=self.template_searchpaths)
        template = env.get_template(template_name)
        return template.render(context)

    def _render_to_file(self, template_name: str, context: dict[str, Any], file_name: str) -> Path:
        """Render text with Jinja2 and save it to the file."""
        path = Path(file_name)
        text = self._render_to_text(template_name, context)
        with path.open("w") as f:
            f.write(text)
        return path

    def _check_register_map(self) -> None:
        """Check if the register map contains unsupported features.

        Every generator should at least support flatmap with registers.
        Child generator can override this method to check for more specific features or relax the checks.

        Raises:
            GeneratorUnsupportedFeatureError: If the register map contains unsupported features.

        """
        if self.register_map.has_maps:
            raise GeneratorUnsupportedFeatureError(self, "maps inside register map")

        if self.register_map.has_map_arrays:
            raise GeneratorUnsupportedFeatureError(self, "map arrays inside register map")

        if self.register_map.has_memories:
            raise GeneratorUnsupportedFeatureError(self, "memories inside register map")

        if self.register_map.has_memory_arrays:
            raise GeneratorUnsupportedFeatureError(self, "memory arrays inside register map")

        if self.register_map.has_register_arrays:
            raise GeneratorUnsupportedFeatureError(self, "register arrays inside register map")

    @abstractmethod
    def _generate(self) -> TypeGenerator[Path, None, None]:
        """Generate all the outputs.

        Method should yield paths to the every generated file.
        Method is called within the output directory, so all the paths are relative to it.
        """

    @classmethod
    @abstractmethod
    def get_config_cls(cls) -> type[GeneratorConfig]:
        """Get the configuration class for the generator."""


class ResetStyle(str, Enum):
    """Flip-flop reset style."""

    SYNC_POS = "sync_pos"
    """Synchronous active high reset."""

    SYNC_NEG = "sync_neg"
    """Synchronous active low reset."""

    ASYNC_POS = "async_pos"
    """Asynchronous active high reset."""

    ASYNC_NEG = "async_neg"
    """Asynchronous active low reset."""
