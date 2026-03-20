#!/bin/bash

# Delete venv (if it exists)
if [ -d ".venv" ]; then
    rm -rf .venv
fi

# Create venv
python3 -m venv .venv

# Activate venv
source .venv/bin/activate

# Install packages
pip install -r requirements.txt

# Set AWS environment variables
export AWS_DEFAULT_REGION=us-west-2
export AWS_REGION=us-west-2

echo "Virtual environment setup complete!"
echo "AWS Region has been set to us-west-2."
