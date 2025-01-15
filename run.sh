#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Check if the script is being run from the correct directory
if [ ! -f "app.py" ]; then
    echo "Error: app.py not found in the current directory. Please run this script from the application's root directory."
    exit 1
fi

# Check and activate the virtual environment
if [ -d "venv" ] && [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
    echo "Virtual environment activated."
else
    echo "Error: Virtual environment not found. Please ensure 'venv' exists and is properly set up."
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

# Print a message with the environment variables
echo "Starting the application with the following settings:"
echo "FLASK_HOST=$FLASK_HOST"
echo "FLASK_PORT=$FLASK_PORT"
echo "FLASK_DEBUG=$FLASK_DEBUG"
echo "REDISHOST=$REDISHOST"
echo "REDISPORT=$REDISPORT"
echo "IS_RASPBERRY=$IS_RASPBERRY"

python app.py
# Run the Python application using Gunicorn
# gunicorn --bind "$FLASK_HOST:$FLASK_PORT" "app:create_app()"

