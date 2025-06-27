#!/bin/sh

# This script ensures the database is initialized before starting the main application.

echo "Initializing database..."
# Use flask command to run our custom init-db command from app.py
flask init-db

echo "Starting Gunicorn server..."
# Use exec to replace the shell process with the Gunicorn process.
# This is important for proper signal handling (e.g., when Docker stops the container).
exec gunicorn --bind 0.0.0.0:5000 --preload "app:app"
