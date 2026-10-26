#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
. venv/bin/activate
if [ ! -f .env ]; then
  echo "Missing .env: copy .env.example to .env and fill in required values."
  exit 1
fi
python controller.py
