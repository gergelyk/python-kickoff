#!/usr/bin/env bash

# Enable strict mode
set -euo pipefail

echo "Preparing environment..."

VENV_DIR=venv

echo "Creating python venv..."
python3 -m venv --clear $VENV_DIR

set +u # workaround for a bug in venv (see: https://github.com/pypa/virtualenv/issues/150)
source $VENV_DIR/bin/activate
set -u

echo "Installing required packages..."
pip install --upgrade pip
pip install -r requirements.txt
pip install --no-deps -e .

echo -en "\033[0;32m" # green font
echo "Setup done!"
echo "Invoke the following to activate your venv:"
echo "source $VENV_DIR/bin/activate"
echo -en "\033[0m" # reset font
