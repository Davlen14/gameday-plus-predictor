#!/bin/bash
# Railway build script

# Install Python dependencies  
echo "Installing Python dependencies..."
python3 -m pip install -r requirements.txt

# Install Node dependencies and build React
echo "Building React frontend..."
cd frontend
npm install  
npm run build
cd ..

echo "Build completed successfully!"