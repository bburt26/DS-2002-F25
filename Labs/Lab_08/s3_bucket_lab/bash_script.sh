#!/bin/bash

if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <local-file> <bucket-name> <expiration_seconds>"
    exit 1
fi

LOCAL_FILE=$1
BUCKET=$2
EXPIRATION=$3

if [ ! -f "$LOCAL_FILE" ]; then
    echo "Error: File '$LOCAL_FILE' does not exist."
    exit 1
fi

echo "Uploading $LOCAL_FILE to s3://$BUCKET/ ..."
aws s3 cp "$LOCAL_FILE" "s3://$BUCKET/"

if [ $? -ne 0 ]; then
    echo "Upload failed."
    exit 1
fi

echo "Generating presigned URL with expiration = $EXPIRATION seconds ..."
PRESIGNED_URL=$(aws s3 presign "s3://$BUCKET/$LOCAL_FILE" --expires-in $EXPIRATION)

echo "Presigned URL:"
echo "$PRESIGNED_URL"
