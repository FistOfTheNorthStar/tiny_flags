#!/bin/bash

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR" || exit

echo "Installing development dependencies..."
pip install -e ".[dev]"

echo -e "\nRunning linters..."
for tool in flake8 black isort; do
    echo -e "\nRunning $tool..."
    $tool src tests
done

echo "Run pytest"
pytest tests/