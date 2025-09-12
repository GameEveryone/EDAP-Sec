#!/bin/bash
# Install dependencies and run the FastAPI server

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Starting FastAPI server at http://127.0.0.1:8000 ..."
uvicorn decryption_api:app --reload --host 0.0.0.0 --port 8000
