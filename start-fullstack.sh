#!/bin/bash

# 🚀 Gameday+ - The Ultimate Full Stack Launcher with Health Checks

set -e  # Exit on any error

echo "🏈 Preparing Gameday+ Development Environment..."

# --- Pre-flight Checks ---
if [ ! -f "app.py" ]; then
    echo "❌ Error: Please run this script from the project's root directory (where app.py is located)."
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

# Check if ports are already in use
echo "🔍 Checking port availability..."

if lsof -Pi :5002 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo "⚠️  Port 5002 is already in use"
    echo "   Run: lsof -ti :5002 | xargs kill -9"
    echo "   Or choose a different port"
    read -p "   Kill existing process on port 5002? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        lsof -ti :5002 | xargs kill -9 2>/dev/null || true
        echo "   ✅ Cleared port 5002"
        sleep 1
    else
        exit 1
    fi
fi

if lsof -Pi :5173 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo "⚠️  Port 5173 is already in use"
    echo "   Run: lsof -ti :5173 | xargs kill -9"
    read -p "   Kill existing process on port 5173? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        lsof -ti :5173 | xargs kill -9 2>/dev/null || true
        echo "   ✅ Cleared port 5173"
        sleep 1
    else
        exit 1
    fi
fi

echo "✅ Ports 5002 and 5173 are available"
echo ""

# Get the absolute path to the project for the new terminal tabs
BASE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

echo "🚀 Launching development environment in separate terminal tabs..."

# Create log directory
mkdir -p "$BASE_DIR/logs"

# Use osascript to control the macOS Terminal
osascript <<EOF
tell application "Terminal"
    activate

    -- Start backend in first window/tab
    do script "cd '$BASE_DIR' && echo '🐍 Starting Flask Backend...' && source .venv/bin/activate && echo '   ✅ Virtual environment activated' && python app.py 2>&1 | tee logs/backend.log"

    -- Wait a moment before starting frontend
    delay 2

    -- Open a new window for frontend
    do script "cd '$BASE_DIR/frontend' && echo '🎨 Starting React Frontend...' && export PATH=\"/opt/homebrew/bin:\$PATH\" && npm run dev 2>&1 | tee ../logs/frontend.log"

end tell
EOF

echo ""
echo "⏳ Waiting for servers to start..."
sleep 3

# Health check function
check_server() {
    local url=$1
    local name=$2
    local max_attempts=10
    local attempt=1

    while [ $attempt -le $max_attempts ]; do
        if curl -s -f -o /dev/null "$url"; then
            echo "   ✅ $name is responding at $url"
            return 0
        fi
        echo "   ⏳ Attempt $attempt/$max_attempts: Waiting for $name..."
        sleep 1
        ((attempt++))
    done

    echo "   ❌ $name failed to start at $url"
    return 1
}

echo ""
echo "🔍 Running health checks..."

# Check backend
if check_server "http://localhost:5002/health" "Flask Backend"; then
    BACKEND_OK=true
else
    BACKEND_OK=false
    echo "   💡 Check logs/backend.log for errors"
fi

# Check frontend
if check_server "http://localhost:5173" "React Frontend"; then
    FRONTEND_OK=true
else
    FRONTEND_OK=false
    echo "   💡 Check logs/frontend.log for errors"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ "$BACKEND_OK" = true ] && [ "$FRONTEND_OK" = true ]; then
    echo "🎉 SUCCESS! Both servers are running!"
    echo ""
    echo "📍 Access your application:"
    echo "   🌐 Frontend:  http://localhost:5173"
    echo "   🔧 Backend:   http://localhost:5002"
    echo "   💚 Health:    http://localhost:5002/health"
    echo ""
    echo "📋 Logs saved to:"
    echo "   Backend:  logs/backend.log"
    echo "   Frontend: logs/frontend.log"
else
    echo "⚠️  PARTIAL START - Some servers failed"
    [ "$BACKEND_OK" = false ] && echo "   ❌ Backend: Check logs/backend.log"
    [ "$FRONTEND_OK" = false ] && echo "   ❌ Frontend: Check logs/frontend.log"
fi

echo ""
echo "💡 Each server runs in its own terminal tab for clean, separate logs."
echo "🛑 To stop servers: Use Ctrl+C in each tab individually."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"