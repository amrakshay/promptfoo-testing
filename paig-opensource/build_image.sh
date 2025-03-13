#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Extract the version from the Dockerfile
VERSION=$(grep "paig-server==" Dockerfile | awk -F'==' '{print $2}')

# Find the latest .whl file matching the pattern
LATEST_FILE=$(ls -v paig_server-*.whl 2>/dev/null | tail -n 1)

if [ -n "$LATEST_FILE" ]; then
    # Extract the version from the filename
    VERSION=$(echo "$LATEST_FILE" | grep -oP 'paig_server-\K[0-9]+\.[0-9]+\.[0-9]+')
else
    # Prompt user for version if no file is found
    read -p "No paig_server-*.whl file found. Enter version manually: " VERSION
fi

echo "Version: $VERSION"

# Define the image name
IMAGE_NAME="paig-opensource-server:$VERSION"

ENV_FILE=".env"

# Create .env file if it doesn't exist
if [ ! -f "$ENV_FILE" ]; then
    cp sample.env .env
fi

# Check if the variable exists in the file
if grep -q "^VERSION=" "$ENV_FILE"; then
    # Update the existing variable
    sed -i "s|^VERSION=.*|VERSION=\"$VERSION\"|" "$ENV_FILE"
else
    # Append the variable to the file
    echo "VERSION=\"$VERSION\"" >> "$ENV_FILE"
fi

# Build the Docker image
echo "Building Docker image with tag: $IMAGE_NAME"
echo "docker build --build-arg VERSION=$VERSION --no-cache -t $IMAGE_NAME ."
docker build --build-arg VERSION=$VERSION --no-cache -t "$IMAGE_NAME" .

# Print success message
echo "Docker image built and tagged successfully: $IMAGE_NAME"

