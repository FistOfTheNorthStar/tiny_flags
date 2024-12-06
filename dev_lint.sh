#!/bin/bash

echo "Installing development dependencies..."
pip install -e ".[dev]"

echo -e "\nRunning linters..."
for tool in flake8 black isort; do
    echo -e "\nRunning $tool..."
    $tool src tests
done