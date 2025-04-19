"""Base classes for all generators."""

from __future__ import annotations

import contextlib
import importlib.util
import os
from abc import ABC, abstractmethod
from enum import Enum
from pathlib import Path
from typing import TYPE_CHECKING, Any, Literal

if TYPE_CHECKING:
    from collections.abc import Generator as TypeGenerator

    from corsair._model import Map

import jinja2
from pydantic import BaseModel, ConfigDict, Field

from corsair._templates import TemplateEnvironment
from corsair._types import PyAttrPathStr


@contextlib.contextmanager
def _change_workdir(path: Path) -> TypeGenerator[None, None, None]:
    old_cwd = Path.cwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(old_cwd)


class GeneratorTemplateError(Exception):
    """Raised when generator fails to render a template."""

    def __init__(self, label: str, j2_error: jinja2.TemplateError) -> None:
        """Initialize the exception."""
        self.label = label
        self.j2_error = j2_error
        super().__init__(f"Generator '{label}' failed to render template")

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


class CustomGeneratorConfig(GeneratorConfig):
    """Custom configuration that is used by custom generator class."""

    kind: Literal["custom"] = "custom"
    """Generator kind discriminator."""

    generator: PyAttrPathStr = Field(..., examples=["bar.py::BarGenerator"])
    """Path to a custom generator class to be used."""

    model_config = ConfigDict(
        extra="allow",
        use_attribute_docstrings=True,
    )

    @property
    def generator_cls(self) -> type[Generator]:
        """Generator class to use."""
        if hasattr(self, "_generator_cls"):
            return self._generator_cls

        module_path, class_name = self.generator.split("::")

        full_path = Path(module_path).resolve()
        spec = importlib.util.spec_from_file_location(full_path.stem, str(full_path))
        if spec is None or spec.loader is None:
            raise ImportError(f"Could not load module from {full_path}")

        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        try:
            loaded_cls = getattr(module, class_name)
        except AttributeError as e:
            raise ImportError(f"Generator class '{class_name}' not found in module '{full_path}'") from e

        if not issubclass(loaded_cls, Generator):
            raise TypeError(f"Class '{class_name}' must be a subclass of 'Generator'")

        self._generator_cls = loaded_cls
        return loaded_cls


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
        self.output_dir = output_dir
        self.template_searchpaths = template_searchpaths

    def __call__(self) -> TypeGenerator[Path, None, None]:
        """Generate all the outputs."""
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Generation is isolated within the output directory
        with _change_workdir(self.output_dir):
            try:
                self._pre_generate()
                yield from self._generate()
            except jinja2.TemplateError as e:
                raise GeneratorTemplateError(self.label, e) from e
            except Exception:
                raise

    def _render_to_text(self, template_name: str, context: dict[str, Any]) -> str:
        """Render text with Jinja2."""
        env = TemplateEnvironment(searchpaths=self.template_searchpaths)
        template = env.get_template(template_name)
        return template.render(context)

    def _render_to_file(self, template_name: str, context: dict[str, Any], file_name: str) -> Path:
        """Render text with Jinja2 and save it to the file."""
        path = self.output_dir / file_name
        text = self._render_to_text(template_name, context)
        with path.open("w") as f:
            f.write(text)
        return path

    @abstractmethod
    def _pre_generate(self) -> None:
        """Pre-generate hook.

        Concrete generator can override this method to perform any necessary
        checking and setup before the generation process begins.
        """

    @abstractmethod
    def _generate(self) -> TypeGenerator[Path, None, None]:
        """Generate all the outputs."""

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
