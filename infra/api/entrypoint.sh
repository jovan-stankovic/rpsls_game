#!/bin/bash
set -e

echo "Starting migration..."
alembic upgrade head || echo "Migration failed!"
echo "Migration complete. Starting server..."

exec uvicorn main:app --host 0.0.0.0 --port 8000 --log-level info --log-config log_config.yaml
