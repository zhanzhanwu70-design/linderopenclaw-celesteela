#!/bin/bash
# Download PTCGP card images from Limitless TCG

SET_CODE=$1
OUTPUT_DIR=${2:-"cards/$SET_CODE"}
MAX_CARDS=${3:-500}

mkdir -p "$OUTPUT_DIR"

echo "Downloading set: $SET_CODE"

# Fetch the card page to get card count
curl -sL "https://pocket.limitlesstcg.com/cards/$SET_CODE" -o /tmp/set_page.html

# Extract card numbers from the page - clean version
CARDS=$(grep -oE "${SET_CODE}_([0-9]+)_EN_SM" /tmp/set_page.html | sed -E "s/${SET_CODE}_([0-9]+)_EN_SM/\1/" | sort -un)

# If no cards found, try alternative method
if [ -z "$CARDS" ]; then
    CARDS=$(grep -oE 'href="/cards/'$SET_CODE'/([0-9]+)"' /tmp/set_page.html | sed -E 's/.*\/([0-9]+)".*/\1/' | sort -un)
fi

CARD_ARRAY=($CARDS)
echo "Found ${#CARD_ARRAY[@]} cards"

COUNT=0
SUCCESS=0
FAIL=0

for CARD_NUM in "${CARD_ARRAY[@]}"; do
    COUNT=$((COUNT + 1))
    if [ $COUNT -gt $MAX_CARDS ]; then
        echo "Max cards reached ($MAX_CARDS)"
        break
    fi
    
    # Remove leading zeros using parameter expansion
    NUM=$(echo "$CARD_NUM" | sed 's/^0*//')
    if [ -z "$NUM" ]; then NUM=0; fi
    # Pad to 3 digits
    NUM=$(printf "%03d" "$NUM")
    
    URL="https://limitlesstcg.nyc3.cdn.digitaloceanspaces.com/pocket/$SET_CODE/${SET_CODE}_${NUM}_EN_SM.webp"
    OUTPUT="$OUTPUT_DIR/${SET_CODE}_${NUM}.webp"
    
    if [ -f "$OUTPUT" ]; then
        echo "Skip: $OUTPUT (exists)"
        SUCCESS=$((SUCCESS + 1))
        continue
    fi
    
    HTTP_CODE=$(curl -sL -o "$OUTPUT" -w "%{http_code}" "$URL")
    
    if [ "$HTTP_CODE" = "200" ]; then
        echo "OK: $OUTPUT"
        SUCCESS=$((SUCCESS + 1))
    else
        rm -f "$OUTPUT"
        echo "FAIL: $URL (HTTP $HTTP_CODE)"
        FAIL=$((FAIL + 1))
        # If we get too many failures in a row, stop
        if [ $FAIL -gt 20 ]; then
            echo "Too many failures, stopping."
            break
        fi
    fi
done

echo ""
echo "Done! Success: $SUCCESS, Failed: $FAIL, Total: $COUNT"
