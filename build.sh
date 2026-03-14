#!/usr/bin/env bash
set -o errexit
set -o pipefail
set -x

# Upgrade pip/setuptools/wheel
python -m pip install --upgrade pip setuptools wheel

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate --no-input

# Collect static files
python manage.py collectstatic --no-input

# Optional: Run tests if you have any
# python manage.py test