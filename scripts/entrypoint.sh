#!/bin/bash
# Exit the script if any command fails
set -e

# Run Alembic migrations
alembic upgrade head

# Start the FastAPI app with Uvicorn
exec uvicorn --app-dir ./src main:app --host 0.0.0.0 --port 8080 --reload "$@"