#!/bin/bash
# run.sh - Lance le daemon narrateur
cd "$(dirname "$0")/.."

echo "🎭 Starting Living Narrator daemon..."
echo "   Events: /mnt/c/Users/reyno/OneDrive/Documents/Civ6Narrator/events.jsonl"
echo ""

python daemon.py
