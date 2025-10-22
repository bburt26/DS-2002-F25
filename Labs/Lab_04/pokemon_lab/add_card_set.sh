#!/bin/bash
read -p "Enter the TCG Card Set ID (e.g., base1, base4): " SET_ID

if [ -z "$SET_ID" ]; then
    echo "Error: Set ID cannot be empty." >&2
    exit 1
fi

echo "Fetching local card data for set: $SET_ID ..."

SOURCE_DIR="card_set_lookup"
DEST_DIR="card_set_lookup"

SOURCE_FILE="${SOURCE_DIR}/${SET_ID}.json"
DEST_FILE="${DEST_DIR}/${SET_ID}.json"

if [ ! -f "$SOURCE_FILE" ]; then
    echo "Error: Local file ${SOURCE_FILE} not found. Please make sure ${SET_ID}.json exists in ${SOURCE_DIR}/" >&2
    exit 1
fi

cp "$SOURCE_FILE" "$DEST_FILE"

echo "Card data for set '$SET_ID' has been added to ${DEST_FILE}"
