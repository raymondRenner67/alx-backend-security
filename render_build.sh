#!/usr/bin/env bash
# Render.com build script

set -o errexit  # exit on error

echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Collecting static files..."
python manage.py collectstatic --no-input --settings=settings_prod

echo "Running database migrations..."
python manage.py migrate --no-input --settings=settings_prod

echo "Creating logs directory..."
mkdir -p logs

echo "Build completed successfully!"
