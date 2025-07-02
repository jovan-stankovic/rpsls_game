#!/bin/bash
set -e

export PYTHONPATH=/

# Run pytest
pytest -v /tests
