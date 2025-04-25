#!/bin/bash

# Get the directory where the script is located
SCRIPT_DIR=$(dirname "$0")

# Generate build schema relative to the script's directory
uv run corsair schema build --indent 2 -o "$SCRIPT_DIR/corsair-build-schema.json"

# Generate map schema relative to the script's directory
uv run corsair schema map --indent 2 -o "$SCRIPT_DIR/corsair-map-schema.json"
