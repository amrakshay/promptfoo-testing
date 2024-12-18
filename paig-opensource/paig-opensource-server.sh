STATE=${1}

if [[ $STATE == "start" ]]
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
