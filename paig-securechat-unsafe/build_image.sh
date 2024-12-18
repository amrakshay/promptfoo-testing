#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Extract the version from the Dockerfile
VERSION=$(grep "paig-securechat==" Dockerfile | awk -F'==' '{print $2}')

# Check if the version was found
if [ -z "$VERSION" ]; then
    echo "Error: Version not found in Dockerfile."
    exit 1
fi

# Define the image name
IMAGE_NAME="paig-securechat-server:$VERSION"

# Build the Docker image
echo "Building Docker image with tag: $IMAGE_NAME"
docker build --no-cache -t "$IMAGE_NAME" .

# Print success message
echo "Docker image built and tagged successfully: $IMAGE_NAME"

