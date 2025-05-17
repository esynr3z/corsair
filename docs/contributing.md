---
icon: material/star-plus
---

# Contributing

This document provides guidelines for contributing to the Corsair project.

## Getting Started

The recommended way to develop Corsair is using the provided Devcontainer configuration, which ensures a consistent environment with all necessary dependencies.

### Option 1: VS Code + Dev Containers (Recommended)

1.  **Prerequisites**: Install [Docker Desktop](https://www.docker.com/products/docker-desktop/) and [Visual Studio Code](https://code.visualstudio.com/) with the [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers).
2.  **Clone the repository**: `git clone https://github.com/esynr3z/corsair.git`
3.  **Open in VS Code**: Open the cloned `corsair` folder in VS Code.
4.  **Reopen in Container**: VS Code should prompt you to "Reopen in Container". Click it. Alternatively, open the Command Palette (`Ctrl+Shift+P` or `Cmd+Shift+P`), search for "Dev Containers: Reopen in Container", and run the command.
5.  **Wait**: The first time, it will take a few minutes to build the Docker image and set up the container.
6.  **Verify**: Once the container is ready, open a terminal within VS Code (`Terminal > New Terminal`). It should open inside the dev container. Verify by running:
    ```bash
    uv run corsair --help
    ```
    You should see the Corsair CLI help message.

### Option 2: Using Docker CLI

1.  **Prerequisites**: Install [Docker](https://docs.docker.com/engine/install/).
2.  **Clone the repository**: `git clone https://github.com/esynr3z/corsair.git`
3.  **Navigate**: `cd corsair`
4.  **Build the image**: Build the Docker image using the provided Dockerfile.
    ```bash
    docker build -t corsair-dev .devcontainer/
    ```
5.  **Run the container**: Start an interactive container, mounting the project directory.

    === "Linux/macOS"
        ```bash
        docker run -it --rm -v "$(pwd):/workspaces/corsair" -w /workspaces/corsair corsair-dev bash
        ```
    === "Windows (Command Prompt)"
        ```bash
        docker run -it --rm -v "%cd%:/workspaces/corsair" -w /workspaces/corsair corsair-dev bash
        ```
    === "Windows (PowerShell)"
        ```bash
        docker run -it --rm -v "${PWD}:/workspaces/corsair" -w /workspaces/corsair corsair-dev bash
        ```

    *   `-it`: Interactive terminal.
    *   `--rm`: Remove the container when it exits.
    *   `-v "...:/workspaces/corsair"`: Mounts your local project directory into the container.
    *   `-w /workspaces/corsair`: Sets the working directory inside the container.
    *   `corsair-dev`: The image name we built.
    *   `bash`: The command to run inside the container.
6.  **Setup Environment**: Inside the container's bash prompt, install dependencies and pre-commit hooks:
    ```bash
    uv sync --all-extras --dev
    uv run poe install-hooks
    ```
7.  **Verify**: Inside the container's bash prompt, run:
    ```bash
    uv run corsair --help
    ```
    You should see the Corsair CLI help message.

### Running Commands

Once inside the development environment (either VS Code terminal or Docker bash), use `uv run` to execute commands within the project's managed Python environment. This ensures you are using the correct dependencies.

For example, to run `pytest`:
```bash
uv run pytest
```

### Available Tasks (Poe the Poet)

Common development tasks are defined using [poethepoet](https://github.com/nat-n/poethepoet) and can be run via `uv run poe <task_name>`. You can list all available tasks with:

```bash
uv run poe
```

Common tasks include:

* `clean`: Clean project directory from temporary files and folders
* `install-hooks`: Install Git pre-commit hooks
* `format`: Format all the Python code with Ruff
* `lint`: Lint all the Python code with Ruff
* `fix-lint`: Lint all the Python code with Ruff and fix the issues
* `check-format`: Check format for all the Python code with Ruff
* `check-types`: Do type checking for all the Python code with Pyright
* `test`: Run all tests via pytest
* `test-cov`: Run all tests via pytest with coverage collection
* `check-commits`: Do commit message checking for the current branch
* `docs`: Build the documentation
* `serve-docs`: Run development server for the documentation development

## Project Choices

To ensure consistency and maintainability, the Corsair project relies on a specific set of tools and conventions. Understanding these choices is crucial for effective contribution.

### Main Dependencies

*   **CLI Management**: [Typer](https://typer.tiangolo.com/)
*   **Data Management**: [Pydantic](https://docs.pydantic.dev/)
*   **Templating**: [Jinja2](https://jinja.palletsprojects.com/)

### Python Infrastructure

*   **Python Version**: Requires [Python](https://www.python.org/) 3.10 or newer.
*   **Package Management**: [uv](https://github.com/astral-sh/uv)
*   **Task Management**: [poethepoet](https://github.com/nat-n/poethepoet) (tasks defined in `pyproject.toml`)
*   **Formatting**: [Ruff Formatter](https://docs.astral.sh/ruff/formatter/)
*   **Linting**: [Ruff Linter](https://docs.astral.sh/ruff/linter/)
*   **Type Checking**: [Pyright](https://github.com/microsoft/pyright)
*   **Unit Testing**: [pytest](https://docs.pytest.org/)

### HDL Infrastructure

*   **Unit Testing**: [cocotb](https://www.cocotb.org/)
*   **Verilog/SystemVerilog Simulators**: [Verilator](https://verilator.org/) (open-source) and Modelsim (commercial).
*   **VHDL Simulators**: [GHDL](https://ghdl.github.io/ghdl/) (open-source) and Modelsim (commercial).
*   **Formal Verification**: [EQY (Yosys-SMTBMC)](https://github.com/YosysHQ/eqy)

### Documentation

*   **Generator**: [MkDocs](https://www.mkdocs.org/)
*   **Theme**: [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)
*   **Hosting**: [GitHub Pages](https://pages.github.com/)

### Git Workflow

*   **Branching**: A single `master` branch holds the stable code. Development happens in short-lived feature branches branched off `master`.
*   **Commits**: Follow the [Conventional Commits](https://www.conventionalcommits.org/) specification (checked via [Commitizen](https://commitizen-tools.github.io/commitizen/)).
*   **Tags**: Follow [Semantic Versioning (SemVer)](https://semver.org/).
*   **Hooks**: [pre-commit](https://pre-commit.com/) (configured in `.pre-commit-config.yaml`).
*   **Changelog**: Follow the [Keep a Changelog](https://keepachangelog.com/) format (in `CHANGELOG.md`).

### Automation

*   **Continuous Integration (CI)**: [GitHub Actions](https://github.com/features/actions) (configured in `.github/workflows/`).
*   **Development Environment**: [Devcontainer](https://containers.dev/) (configured in `.devcontainer/devcontainer.json`).
