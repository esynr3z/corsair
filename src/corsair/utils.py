#!/usr/bin/env python3

"""Utility functions and classes."""

from __future__ import annotations

import os
from contextlib import contextmanager
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Iterator


@contextmanager
def chdir(path: Path) -> Iterator[None]:
    """Temporarily change directory for the context."""
    oldpwd = Path.cwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(oldpwd)


def resolve_path(p: Path) -> Path:
    """Get absolute path resolving any inderiction."""
    return p.expanduser().resolve(strict=False)
