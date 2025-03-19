STATE=${1}

if [[ $STATE == "setup" ]]
then
  ENV_FILE=".env"

  # Create .env file if it doesn't exist
  if [ ! -f "$ENV_FILE" ]; then
      echo "Creating $ENV_FILE..."
      cp sample.env .env
      echo "Please fill in the required environment variables in $ENV_FILE."
  fi
elif [[ $STATE == "start" ]]
then
  echo "Starting paig-securechat-server"

  TARGET_DIR="custom-configs"
  echo "Scanning directory: $TARGET_DIR for JSON files..."

  # Define source and replacement strings
  SOURCE_STRING='"shieldServerUrl": "http://127.0.0.1:4545"'
  REPLACEMENT_STRING='"shieldServerUrl": "http://paig-opensource-container:4545"'

  # Find all JSON files and replace the shieldServerUrl
  find "$TARGET_DIR" -type f -name "*.json" | while read -r file; do
      if grep -q "$SOURCE_STRING" "$file"; then
          echo "Updating: $file"
          echo "Replacing: $SOURCE_STRING"
          echo "With:      $REPLACEMENT_STRING"
          sed -i "s#$SOURCE_STRING#$REPLACEMENT_STRING#g" "$file"
      fi
  done

  echo "Replacement completed successfully!"

  docker-compose up -d
elif [[ $STATE == "stop" ]]
then
  echo "Stopping paig-securechat-server"
  docker-compose down
elif [[ $STATE == "logs" ]]
then
  docker logs -f paig-securechat-unsafe-container
elif [[ $STATE == "shell" ]]
then
  docker exec -it paig-securechat-unsafe-container bash
fi
