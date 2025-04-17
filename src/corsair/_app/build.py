"""CLI command to build output files."""

from __future__ import annotations

import logging
import shutil
from pathlib import Path
from typing import Annotated

import typer  # noqa: TCH002

import corsair as csr

# Get logger singleton
log = logging.getLogger("corsair")


def _prepare_output_root(output: Path, clean: bool) -> Path:
    """Prepare the output root directory."""
    resolved_path = output.expanduser().resolve()
    log.debug("Resolved output directory: %s", resolved_path)

    if resolved_path == Path.cwd():
        raise ValueError("In-source builds are not allowed. Output directory cannot be the current working directory.")

    if clean:
        log.debug("Cleaning output directory: %s", resolved_path)
        shutil.rmtree(resolved_path)

    log.debug("Creating output directory: %s", resolved_path)
    resolved_path.mkdir(parents=True, exist_ok=True)

    # Write gitignore file to ignore all output files
    (resolved_path / ".gitignore").write_text("*\n")

    return resolved_path


def build(
    spec: Annotated[
        Path,
        typer.Option("-s", "--spec", show_default=True, help="Path to a build specification file"),
    ] = Path("csrbuild.toml"),
    targets: Annotated[
        list[str] | None,
        typer.Argument(
            show_default=False,
            help="Select targets to build. By default, all targets are built when empty.",
        ),
    ] = None,
    output: Annotated[
        Path,
        typer.Option(
            "-o",
            "--output",
            show_default=True,
            help="Path to an output directory",
        ),
    ] = Path("corsair-build"),
    clean: Annotated[
        bool,
        typer.Option(
            "--clean",
            show_default=False,
            help="Clean the output directory before building.",
        ),
    ] = False,
) -> None:
    """Build required targets according to the provided specification."""
    log.debug("cmd build args: %s", locals())

    if targets is None or "all" in targets:
        targets = ["all"]

    try:
        # Resolve and prepare output directory
        prepared_output_dir = _prepare_output_root(output=output, clean=clean)
        log.info("Output directory: %s", prepared_output_dir)

        log.info("Read build specification")
        build_spec = csr.BuildSpecification.from_toml_file(spec)

        log.info("Available targets: %s", [cfg.label for cfg in build_spec.generators])
        log.info("Targets to build: %s", targets)

        log.info("Load CSR map")
        loader = build_spec.loader.loader_cls(build_spec.loader)
        csr_map = loader()

        for cfg in build_spec.generators:
            if cfg.label in targets or "all" in targets:
                log.info("Generate outputs for '%s'", cfg.label)
                generator = cfg.generator_cls(
                    register_map=csr_map,
                    config=cfg,
                    output_dir=prepared_output_dir / cfg.label,
                )
                for out_file in generator():
                    log.info(out_file)

        log.info("Build completed successfully")

    except Exception as e:
        log.error(e)
        raise RuntimeError("Build failed.") from e
