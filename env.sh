#!/bin/bash

VENV=".venv/filter"
python3 -m venv "$VENV"
source "$VENV/bin/activate"

pip install --upgrade pip

pip install pillow
pip install pytest
pip install mock

echo "source $VENV/bin/activate"