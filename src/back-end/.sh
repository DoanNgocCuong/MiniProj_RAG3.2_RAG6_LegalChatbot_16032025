#!/bin/bash

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    python -m venv .venv
fi

# Activate virtual environment
source .venv/Scripts/activate

# Install requirements if requirements.txt exists
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
fi

echo "Virtual environment setup complete!"


uvicorn rag_backend:app --host 0.0.0.0 --port 30002 --reload --log-level debug