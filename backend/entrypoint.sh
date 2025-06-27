#!/bin/sh

# This script ensures the database is initialized before starting the main application.

echo "Initializing database..."
# Use flask command to run our custom init-db command from app.py
flask init-db

echo "Starting Gunicorn server..."
# MODIFIED: Removed the --preload flag to prevent startup conflicts.
# The database is already initialized by the command above.
exec gunicorn --bind 0.0.0.0:5000 "app:app"
