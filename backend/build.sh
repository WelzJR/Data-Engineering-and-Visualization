#!/bin/bash
set -o errexit

echo "Python version: $(python --version)"
echo "Pip version: $(pip --version)"

# Upgrade pip, setuptools, and wheel to latest versions
pip install --upgrade pip setuptools wheel

# Install requirements with preference for binary wheels
pip install --prefer-binary -r requirements.txt
