#!/bin/bash
# foxBMS Documentation Server
# Run this script to view documentation in browser

PORT=8080
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# Server root is docs/ (parent of final/) to access both parvis/ and final/
DOCS_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "========================================"
echo "  foxBMS Documentation Server"
echo "========================================"
echo ""
echo "Starting server at: http://localhost:$PORT/final/"
echo "Documentation root: $DOCS_DIR"
echo "  - final/: Final documentation"
echo "  - parvis/: PARVIS intermediate outputs"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

cd "$DOCS_DIR"

# Try to open browser automatically
if command -v xdg-open &> /dev/null; then
    (sleep 1 && xdg-open "http://localhost:$PORT/final/") &
elif command -v open &> /dev/null; then
    (sleep 1 && open "http://localhost:$PORT/final/") &
fi

# For WSL - try to open Windows browser
if grep -qi microsoft /proc/version 2>/dev/null; then
    echo "WSL detected. Opening in Windows browser..."
    (sleep 1 && cmd.exe /c start "http://localhost:$PORT/final/") &
fi

python3 -m http.server $PORT
