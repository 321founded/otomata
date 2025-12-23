#!/bin/bash
set -e
PORT=8020
cd "$(dirname "$0")/.."
echo "Demarrage Otomata sur port ${PORT}"
unbuffer ../venv/bin/python manage.py runserver "0.0.0.0:${PORT}" 2>&1 | tee dev/dev.log
