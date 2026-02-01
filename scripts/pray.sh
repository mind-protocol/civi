#!/bin/bash
# pray.sh - Envoie une prière/question à Dieu
# Usage: ./scripts/pray.sh "Dieu, dois-je revendiquer des terres?"

cd "$(dirname "$0")/.."

PRAYERS_FILE="narrator/state/prayers.jsonl"

if [ -z "$1" ]; then
    echo "Usage: ./scripts/pray.sh \"Ta prière ici\""
    echo ""
    echo "Exemples:"
    echo "  ./scripts/pray.sh \"Dieu, dois-je accepter ce mariage?\""
    echo "  ./scripts/pray.sh \"Seigneur, que penses-tu de mon frère?\""
    exit 1
fi

PRAYER="$*"
TIMESTAMP=$(date -Iseconds)

# Create prayer entry
echo "{\"timestamp\": \"$TIMESTAMP\", \"speaker\": \"jesus\", \"type\": \"prayer\", \"text\": \"$PRAYER\"}" >> "$PRAYERS_FILE"

echo "🙏 Prière envoyée:"
echo "   \"$PRAYER\""
echo ""
echo "Dieu la verra lors de la prochaine narration."
