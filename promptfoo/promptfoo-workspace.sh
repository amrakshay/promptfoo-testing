STATE=${1}

if [[ $STATE == "start" ]]
then
  echo "Starting promptfoo-workspace"
  docker-compose up -d
elif [[ $STATE == "stop" ]]
then
  echo "Stopping promptfoo-workspace"
  docker-compose down
elif [[ $STATE == "logs" ]]
then
  docker logs -f promptfoo-workspace-container
elif [[ $STATE == "shell" ]]
then
  docker exec -it promptfoo-workspace-container bash
fi
