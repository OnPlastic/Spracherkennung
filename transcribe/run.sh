#!/usr/bin/env bash
cd "$(dirname "$0")" || exit 1
source activate.sh >/dev/null
PYTHONPATH=src python -m transcribe_cli.main
