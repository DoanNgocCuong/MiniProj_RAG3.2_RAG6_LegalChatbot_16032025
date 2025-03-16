#!/bin/bash

# Activate virtual environment if exists
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# Install requirements if needed
pip install -r backend_vector_database/requirements_backend.txt

# Start the backend server
python -m backend_vector_database.rag_backend 