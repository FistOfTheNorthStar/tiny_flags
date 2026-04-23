#!/bin/bash

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR" || exit

VENV_DIR="$SCRIPT_DIR/.venv"

# Create venv if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
fi

# Activate venv
source "$VENV_DIR/bin/activate"

echo "Installing development dependencies..."
pip install -e ".[dev]"

echo -e "\nRunning ruff..."
ruff check src/ tests/

echo -e "\nRunning ruff format check..."
ruff format --check src/ tests/

echo -e "\nRunning mypy..."
mypy src/

echo -e "\nRunning pytest..."
pytest --cov=tiny_flags --cov-report=term-missing