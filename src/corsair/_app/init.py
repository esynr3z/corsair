"""CLI commands to initialize an example project."""

from __future__ import annotations

import importlib.util
import logging
from enum import Enum
from pathlib import Path
from typing import TYPE_CHECKING, Annotated

import typer  # noqa: TCH002

import corsair as csr

# Get logger singleton
log = logging.getLogger("corsair")


class TemplateKind(str, Enum):
    """Template kind."""

    JSON = "json"
    """JSON project template."""

    HJSON = "hjson"
    """HJSON project template."""

    YAML = "yaml"
    """YAML project template."""

    def __str__(self) -> str:
        """Return string representation of template kind."""
        return self.value


def _dump(kind: TemplateKind, path: Path, data: dict) -> None:
    """Dump data to a file of given kind."""
    log.info("Dumping data to %s", path)
    with path.open("w", encoding="utf-8") as f:
        if kind == TemplateKind.YAML:
            import yaml

            yaml.dump(data, f)
        elif kind == TemplateKind.HJSON:
            import hjson

            hjson.dump(data, f)
        elif kind == TemplateKind.JSON:
            import json

            json.dump(data, f)


def _create_buildspec(kind: TemplateKind) -> csr.BuildSpecification:
    """Create example build specification."""
    wavedrom_available = importlib.util.find_spec("wavedrom") is not None

    if kind == TemplateKind.YAML:
        loader = csr.SerializedLoader.Config(kind="yaml")
    elif kind == TemplateKind.HJSON:
        loader = csr.SerializedLoader.Config(kind="hjson")
    else:
        loader = csr.SerializedLoader.Config(kind="json")

    generators = {}
    generators["doc_markdown"] = csr.MarkdownGenerator.Config(
        print_images=wavedrom_available, wavedrom=csr.WaveDromGenerator.Config(lanes=2)
    )
    if wavedrom_available:
        generators["doc_wavedrom"] = csr.WaveDromGenerator.Config(dump_json=True, lanes=2)

    return csr.BuildSpecification(
        loader=loader,
        generators=generators,
    )


def _create_regmap() -> csr.Map:
    """Generate example register map."""
    regs = []

    regs.append(
        csr.Register(
            name="DATA",
            doc="Data register",
            offset=0x4,
            fields=(
                csr.Field(
                    name="FIFO",
                    doc="Write to push value to TX FIFO, read to get data from RX FIFO",
                    width=8,
                    offset=0,
                    access=csr.AccessMode.RW,
                    hardware=csr.HardwareMode.Q,
                    reset=None,
                ),
                csr.Field(
                    name="FERR",
                    doc="Frame error flag. Read to clear.",
                    width=1,
                    offset=16,
                    access=csr.AccessMode.ROLH,
                    hardware=csr.HardwareMode.I,
                    reset=None,
                ),
                csr.Field(
                    name="PERR",
                    doc="Parity error flag. Read to clear.",
                    width=1,
                    offset=17,
                    access=csr.AccessMode.ROLH,
                    hardware=csr.HardwareMode.I,
                    reset=None,
                ),
            ),
        )
    )

    regs.append(
        csr.Register(
            name="STAT",
            doc="Status register",
            offset=0xC,
            fields=(
                csr.Field(
                    name="BUSY",
                    doc="Transciever is busy",
                    width=1,
                    offset=2,
                    access=csr.AccessMode.RO,
                    hardware=csr.HardwareMode("ie"),
                    reset=None,
                ),
                csr.Field(
                    name="RXE",
                    doc="RX FIFO is empty",
                    width=1,
                    offset=4,
                    access=csr.AccessMode.RO,
                    hardware=csr.HardwareMode.I,
                    reset=None,
                ),
                csr.Field(
                    name="TXF",
                    doc="TX FIFO is full",
                    width=1,
                    offset=8,
                    access=csr.AccessMode.RO,
                    hardware=csr.HardwareMode.I,
                    reset=None,
                ),
            ),
        )
    )

    regs.append(
        csr.Register(
            name="CTRL",
            doc="Control register",
            offset=0x10,
            fields=(
                csr.Field(
                    name="BAUD",
                    doc="Baudrate value",
                    width=2,
                    offset=0,
                    access=csr.AccessMode.RW,
                    hardware=csr.HardwareMode.O,
                    reset=2,
                    enum=csr.Enum(
                        name="BAUD_ENUM",
                        doc="Baudrate enumeration",
                        members=(
                            csr.EnumMember(name="B9600", value=0, doc="9600 baud"),
                            csr.EnumMember(name="B38400", value=1, doc="38400 baud"),
                            csr.EnumMember(name="B115200", value=2, doc="115200 baud"),
                        ),
                    ),
                ),
                csr.Field(
                    name="TXEN",
                    doc="Transmitter enable. Can be disabled by hardware on error.",
                    width=1,
                    offset=4,
                    access=csr.AccessMode.RW,
                    hardware=csr.HardwareMode("oie"),
                    reset=0,
                ),
                csr.Field(
                    name="RXEN",
                    doc="Receiver enable. Can be disabled by hardware on error.",
                    width=1,
                    offset=5,
                    access=csr.AccessMode.RW,
                    hardware=csr.HardwareMode("oie"),
                    reset=0,
                ),
                csr.Field(
                    name="TXST",
                    doc="Force transmission start",
                    width=1,
                    offset=6,
                    access=csr.AccessMode.WOSC,
                    hardware=csr.HardwareMode.O,
                    reset=None,
                ),
            ),
        )
    )

    regs.append(
        csr.Register(
            name="LPMODE",
            doc="Low power mode control",
            offset=0x14,
            fields=(
                csr.Field(
                    name="DIV",
                    doc="Clock divider in low power mode",
                    width=8,
                    offset=0,
                    access=csr.AccessMode.RW,
                    hardware=csr.HardwareMode.O,
                    reset=0,
                ),
                csr.Field(
                    name="EN",
                    doc="Low power mode enable",
                    width=1,
                    offset=31,
                    access=csr.AccessMode.RW,
                    hardware=csr.HardwareMode.O,
                    reset=1,
                ),
            ),
        )
    )

    regs.append(
        csr.Register(
            name="INTSTAT",
            doc="Interrupt status register",
            offset=0x20,
            fields=(
                csr.Field(
                    name="TX",
                    doc="Transmitter interrupt flag. Write 1 to clear.",
                    width=1,
                    offset=0,
                    access=csr.AccessMode.RW1C,
                    hardware=csr.HardwareMode.S,
                    reset=0,
                ),
                csr.Field(
                    name="RX",
                    doc="Receiver interrupt. Write 1 to clear.",
                    width=1,
                    offset=1,
                    access=csr.AccessMode.RW1C,
                    hardware=csr.HardwareMode.S,
                    reset=0,
                ),
            ),
        )
    )

    regs.append(
        csr.Register(
            name="ID",
            doc="IP-core ID register",
            offset=0x40,
            fields=(
                csr.Field(
                    name="UID",
                    doc="Unique ID",
                    width=32,
                    offset=0,
                    access=csr.AccessMode.RO,
                    hardware=csr.HardwareMode.F,
                    reset=0xCAFE0666,
                ),
            ),
        )
    )

    return csr.Map(
        name="uart",
        doc="UART register map",
        offset=0x0,
        address_width=12,
        register_width=32,
        items=tuple(regs),
    )


def init(
    kind: Annotated[
        TemplateKind,
        typer.Argument(
            help="Template kind. Defines the format of the generated register map file.",
            show_choices=True,
            show_default=True,
        ),
    ] = TemplateKind.YAML,
    output: Annotated[
        Path,
        typer.Option(
            "-o",
            "--output",
            show_default=True,
            help="Path to an output directory",
        ),
    ] = Path(),
) -> None:
    """Initialize a simple project."""
    log.debug("cmd init args: %s", locals())

    # Check if hjson is installed
    if kind == TemplateKind.HJSON and importlib.util.find_spec("hjson") is None:
        raise ImportError(
            "hjson is not installed. "
            "Try installing it with `pip install corsair[hjson]` or `pip install corsair[full]`."
        )

    # Create output directory
    output.mkdir(parents=True, exist_ok=True)

    # Dump files
    _dump(TemplateKind.YAML, output / "csrbuild.yaml", _create_buildspec(kind).model_dump(mode="json"))
    _dump(kind, output / f"csrmap.{kind.value.lower()}", _create_regmap().model_dump(mode="json"))
