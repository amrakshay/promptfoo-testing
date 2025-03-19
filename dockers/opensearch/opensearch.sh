STATE=${1}

ENV_FILE=".env"

# Create .env file if it doesn't exist
if [ ! -f "$ENV_FILE" ]; then
    cp sample.env .env
fi

if [[ $STATE == "start" ]]
then
  sudo sysctl -w vm.max_map_count=262144
  echo "Starting opensearch"
  docker-compose up -d
elif [[ $STATE == "stop" ]]
then
  echo "Stopping opensearch"
  docker-compose down
elif [[ $STATE == "logs" ]]
then
  docker logs -f opensearch-node1
elif [[ $STATE == "shell" ]]
then
  docker exec -it opensearch-node1 bash
fi
