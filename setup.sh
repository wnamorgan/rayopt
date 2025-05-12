#!/bin/bash

set -e

ENV_NAME="rayopt-env"
RAYOPT_PATH="./rayopt"  # Adjust if your repo is elsewhere

echo "Creating virtual environment..."
python3 -m venv "$ENV_NAME"

echo "Activating virtual environment..."
source "$ENV_NAME/bin/activate"

echo "Upgrading pip..."
pip install --upgrade pip

echo "Installing build dependencies: numpy and cython..."
pip install numpy cython

echo "Installing rayopt in editable mode..."
pip install -e "$RAYOPT_PATH"

# Optional extras
pip install notebook matplotlib

# Save environment snapshot
pip freeze > requirements_rayopt.txt

echo ""
echo "✅ Setup complete."
echo "To activate later, run: source $ENV_NAME/bin/activate"
