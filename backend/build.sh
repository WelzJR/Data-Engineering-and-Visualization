#!/bin/bash
set -o errexit

echo "Python version: $(python --version)"
echo "Pip version: $(pip --version)"

pip install --upgrade pip
pip install -r requirements.txt
