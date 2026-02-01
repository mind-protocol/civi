#!/bin/bash
# run.sh - Lance le Living Narrator daemon avec OCR et capture des décisions
cd "$(dirname "$0")"

export PYTHONPATH=$PYTHONPATH:$(pwd):$(pwd)/src

# Detect game from config
GAME=$(python3 -c "import json; print(json.load(open('narrator/state/config.json')).get('game', 'civ6'))" 2>/dev/null || echo "civ6")

echo "🎭 Living Narrator Daemon"
echo "========================="
echo "Game: $GAME"
echo ""

# Check dependencies
if ! python3 -c "import pytesseract" 2>/dev/null; then
    echo "❌ OCR dependencies missing!"
    echo ""
    echo "Install with:"
    echo "  sudo apt install tesseract-ocr tesseract-ocr-fra"
    echo "  pip install pytesseract pillow pynput"
    echo ""
    exit 1
fi

# Parse flags
NO_OCR=false
NO_CLICKS=false
for arg in "$@"; do
    case $arg in
        --no-ocr) NO_OCR=true ;;
        --no-clicks) NO_CLICKS=true ;;
        --minimal) NO_OCR=true; NO_CLICKS=true ;;
    esac
done

# PIDs to cleanup
PIDS=()

cleanup() {
    echo ""
    echo "Stopping background processes..."
    for pid in "${PIDS[@]}"; do
        kill $pid 2>/dev/null
        wait $pid 2>/dev/null
    done
}
trap cleanup EXIT

# Start OCR watcher (unless disabled)
if [[ "$NO_OCR" == "false" ]]; then
    echo "📝 Starting OCR watcher..."
    python3 scripts/ocr_watcher.py --game "$GAME" &
    OCR_PID=$!
    PIDS+=($OCR_PID)
    echo "   OCR PID: $OCR_PID"
    echo "   Interval: 5s"
else
    echo "⚠️  OCR disabled"
fi

# Start click watcher (unless disabled)
if [[ "$NO_CLICKS" == "false" ]]; then
    if python3 -c "import pynput" 2>/dev/null; then
        echo "🖱️  Starting click watcher..."
        python3 scripts/click_watcher.py &
        CLICK_PID=$!
        PIDS+=($CLICK_PID)
        echo "   Click PID: $CLICK_PID"
        echo "   Captures decisions at each click"
    else
        echo "⚠️  Click watcher unavailable (install: pip install pynput)"
    fi
else
    echo "⚠️  Click watcher disabled"
fi

echo ""

# Start daemon
python3 daemon.py
