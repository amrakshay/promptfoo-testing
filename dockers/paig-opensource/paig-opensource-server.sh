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
  echo "Starting paig-opensource-server"
  docker-compose up -d
elif [[ $STATE == "stop" ]]
then
  echo "Stopping paig-opensource-server"
  docker-compose down
elif [[ $STATE == "logs" ]]
then
  docker logs -f paig-opensource-container
elif [[ $STATE == "shell" ]]
then
  docker exec -it paig-opensource-container bash
fi
