#!/bin/bash

echo "Running black..."
black .
echo "-----"

echo "Running mypy..."
mypy .
echo "-----"

echo "Running ruff..."
ruff check . --fix
echo "-----"

echo "Finished"
