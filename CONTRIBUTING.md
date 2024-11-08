# Contributing


## Getting Started

Python 3.10+ has to be available, then run from command line

```bash
# Install uv
pip install uv==0.5.0

# Create virtual environment and install the package and dependencies
uv sync --all-extras --dev

# Install git hooks
uv run poe install-hooks

# Check that Corsair is installed and shows help
uv run corsair
```

Use `uv run` to run anything related to project within prepared virtual environment. You may need this:

* `uv run pre-commit` - run pre-commit checks manually.
* `uv run poe <task>` - run one of project maintenance tasks (lint, format, build documentation, etc.). Run without `<task>` to check what options are available.
