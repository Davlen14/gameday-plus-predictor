#!/bin/bash

# 🚀 Gameday+ - The Ultimate Full Stack Launcher

echo "🏈 Preparing Gameday+ Development Environment..."

# --- Pre-flight Checks ---
if [ ! -f "predictor_engine/app.py" ]; then
    echo "❌ Error: Please run this script from the project's root directory (predictor_engine/app.py should exist)."
    exit 1
fi

if [ ! -d "frontend" ]; then
    echo "❌ Error: The 'frontend' directory was not found."
    exit 1
fi

if [ ! -d ".venv" ]; then
    echo "❌ Error: Python virtual environment '.venv' not found."
    echo "💡 Run 'python -m venv .venv' to create it first."
    exit 1
fi

echo "✅ Found Python backend files"
echo "✅ Found React frontend directory"  
echo "✅ Found Python virtual environment"
echo ""

# Get the absolute path to the project for the new terminal tabs
BASE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

echo "🚀 Launching development environment in separate terminal tabs..."

# Use osascript to control the macOS Terminal
osascript <<EOF
tell application "Terminal"
    activate
    
    -- Start backend in first window/tab
    do script "cd '$BASE_DIR' && echo '🐍 Starting Flask Backend...' && source .venv/bin/activate && echo '   ✅ Virtual environment activated' && python predictor_engine/app.py"
    
    -- Open a new window for frontend
    do script "cd '$BASE_DIR/frontend' && echo '🎨 Starting React Frontend...' && export PATH=\"/opt/homebrew/bin:\$PATH\" && npm run dev"
    
end tell
EOF

echo ""
echo "🎉 Your development environment is launching in a new Terminal window!"
echo ""
echo "📍 Access your application:"
echo "   🌐 React Frontend: http://localhost:5173"
echo "   🔧 Flask Backend:  http://localhost:5002"
echo ""
echo "💡 Each server runs in its own terminal tab for clean, separate logs."
echo "�� To stop servers: Use Ctrl+C in each tab individually."
