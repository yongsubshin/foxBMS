#!/bin/bash
# foxBMS Documentation Server
# Run this script to view documentation in browser

PORT=8080
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "========================================"
echo "  foxBMS Documentation Server"
echo "========================================"
echo ""
echo "Starting server at: http://localhost:$PORT"
echo "Documentation root: $DIR"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

cd "$DIR"

# Try to open browser automatically
if command -v xdg-open &> /dev/null; then
    (sleep 1 && xdg-open "http://localhost:$PORT") &
elif command -v open &> /dev/null; then
    (sleep 1 && open "http://localhost:$PORT") &
fi

# For WSL - try to open Windows browser
if grep -qi microsoft /proc/version 2>/dev/null; then
    echo "WSL detected. Opening in Windows browser..."
    (sleep 1 && cmd.exe /c start "http://localhost:$PORT") &
fi

python3 -m http.server $PORT
