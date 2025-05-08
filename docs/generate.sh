#!/bin/bash

# Get the directory where the script is located
SCRIPT_DIR=$(dirname "$0")

# Generate CLI reference relative to the script's directory
uv run typer corsair._app utils docs --name "corsair" --output "$SCRIPT_DIR/cli.md"
