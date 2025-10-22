#!/bin/bash

echo "Refreshing all card sets in card_set_lookup/ ..."

for FILE in card_set_lookup/*.json; do

    if [ ! -e "$FILE" ]; then
        echo "No JSON files found in card_set_lookup/. Nothing to refresh."
        exit 0
    fi

    SET_ID=$(basename "$FILE" .json)

    echo "Updating set: $SET_ID ..."

    SOURCE_FILE="card_set_lookup/${SET_ID}.json"

    if [ ! -f "$SOURCE_FILE" ]; then
        echo "Warning: No local data found for ${SET_ID}. Skipping."
        continue
    fi

    cp "$SOURCE_FILE" "$FILE"

    echo "Data for ${SET_ID} written to ${FILE}"
done

echo "All card sets in card_set_lookup/ have been refreshed!"
