#!/bin/bash
set -e

# Default port if not set
PORT=${PORT:-8080}

echo "Starting Gameday+ server on port $PORT..."

# Use gunicorn to start the Flask app
exec gunicorn app:app \
    --bind "0.0.0.0:$PORT" \
    --workers 1 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile -