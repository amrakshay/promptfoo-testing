STATE=${1}

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
