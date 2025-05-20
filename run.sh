#!/bin/bash

echo "Starting main application containers trong thư mục src..."
cd src && docker compose up --build -d

echo "Starting LLMs offline containers trong thư mục src/llms-offline..."
cd llms-offline && docker compose up --build -d

echo "Starting database containers trong thư mục DB..."
cd ../../DB && docker compose up --build -d

echo "All containers have been started successfully!"
