#!/bin/bash
# Fetch card data from Limitless TCG and build a database

SET=$1
OUTPUT="memory/cards_${SET}.json"

echo "Fetching card data for $SET..."

# Get total cards from set page
curl -sL "https://pocket.limitlesstcg.com/cards/$SET" -o /tmp/set_page.html
TOTAL=$(grep -oE "${SET}_[0-9]+_EN_SM" /tmp/set_page.html | wc -l)
echo "Total cards: $TOTAL"

# Fetch each card page and extract data
echo "[" > "$OUTPUT"

FIRST=true
for i in $(seq 1 $TOTAL); do
    if [ "$FIRST" = true ]; then
        FIRST=false
    else
        echo "," >> "$OUTPUT"
    fi
    
    echo -n "{\"number\":$i,\"name\":\"" >> "$OUTPUT"
    
    # Fetch card page
    curl -sL "https://pocket.limitlesstcg.com/cards/$SET/$i" -o /tmp/card_page.html
    
    # Extract name from title
    NAME=$(grep -oE '<title>[^<]+</title>' /tmp/card_page.html | sed 's/<title>\([^•]*\).*/\1/' | sed 's/ //g' | sed 's/•.*//')
    echo -n "$NAME" >> "$OUTPUT"
    
    echo -n "\",\"type\":\"" >> "$OUTPUT"
    TYPE=$(grep -oE 'Type:</b>[^<]+' /tmp/card_page.html | sed 's/Type:<\/b>//' | sed 's/ //g')
    echo -n "$TYPE" >> "$OUTPUT"
    
    echo -n "\",\"hp\":\"" >> "$OUTPUT"
    HP=$(grep -oE 'HP:</b>[0-9]+' /tmp/card_page.html | sed 's/HP:<\/b>//')
    echo -n "$HP" >> "$OUTPUT"
    
    echo "\"}" >> "$OUTPUT"
    
    if [ $((i % 20)) -eq 0 ]; then
        echo "Processed $i / $TOTAL"
    fi
    
    # Small delay to be nice to the server
    sleep 0.1
done

echo "]" >> "$OUTPUT"
echo "Done! Data saved to $OUTPUT"
