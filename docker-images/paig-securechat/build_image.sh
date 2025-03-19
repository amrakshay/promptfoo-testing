#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Find the latest .whl file matching the pattern
LATEST_FILE=$(ls -v paig_securechat-*.whl 2>/dev/null | tail -n 1)
USE_LOCAL_WHEEL=false

if [ -n "$LATEST_FILE" ]; then
    # Extract the version from the filename
    VERSION=$(echo "$LATEST_FILE" | grep -oP 'paig_securechat-\K[0-9]+\.[0-9]+\.[0-9]+')
    USE_LOCAL_WHEEL=true
else
    # Prompt user for version if no file is found
    read -p "No paig_securechat-*.whl file found. Enter version manually: " VERSION
fi

echo "Version: $VERSION"

# Define the image name
IMAGE_NAME="paig-securechat-server:$VERSION"

# Create a dummy wheel file if not found
if [ "$USE_LOCAL_WHEEL" != "true" ]; then
    echo "Dummy content for missing wheel file" > ./paig_securechat-${VERSION}-py3-none-any.whl
fi

# Build the Docker image
echo "Building Docker image with tag: $IMAGE_NAME"
echo "docker build --build-arg VERSION=$VERSION --build-arg USE_LOCAL_WHEEL=$USE_LOCAL_WHEEL --no-cache -t $IMAGE_NAME ."
docker build --build-arg VERSION=$VERSION --build-arg USE_LOCAL_WHEEL=$USE_LOCAL_WHEEL --no-cache -t "$IMAGE_NAME" .

# Remove the dummy wheel file
if [ "$USE_LOCAL_WHEEL" != "true" ]; then
    rm ./paig_securechat-${VERSION}-py3-none-any.whl
fi

# Print success message
echo "Docker image built and tagged successfully: $IMAGE_NAME"

