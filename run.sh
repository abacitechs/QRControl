#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Activate the virtual environment
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
    echo "Virtual environment activated."
else
    echo "Virtual environment not found. Please ensure 'venv' exists."
    exit 1
fi

# Export environment variables
export FLASK_HOST='0.0.0.0'
export FLASK_PORT='5000'
export FLASK_DEBUG='false'
export SECRET_KEY='d4e6a4c8b1f2d3c4e5f6a7b8c9d0e1f2a3b4c5d6e7f8g9h0i1j2k3l4m5n6o7p8'
export REDISHOST='127.0.0.1'
export REDISPORT='6379'
export IS_RASPBERRY='true'

# Run the Python application
if [ -f "app.py" ]; then
    python app.py
else
    echo "app.py not found. Please ensure the script exists in the current directory."
    exit 1
fi
