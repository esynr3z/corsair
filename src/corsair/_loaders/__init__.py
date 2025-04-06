"""Loaders for register maps."""

from __future__ import annotations

from typing import Annotated

from pydantic import Field

from .base import CustomLoaderConfig, Loader, LoaderConfig, LoaderValidationError
from .pymodule import PyModuleLoader
from .serialized import SerializedLoader

AnyLoaderConfig = Annotated[
    CustomLoaderConfig | SerializedLoader.Config,
    Field(discriminator="kind"),
]

__all__ = [
    # Base classes
    "Loader",
    "LoaderValidationError",
    "LoaderConfig",
    "CustomLoaderConfig",
    # Loaders
    "SerializedLoader",
    "PyModuleLoader",
    # Types
    "AnyLoaderConfig",
]
