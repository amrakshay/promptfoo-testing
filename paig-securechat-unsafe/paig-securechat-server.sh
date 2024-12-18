STATE=${1}

if [[ $STATE == "start" ]]
then
  echo "Starting paig-securechat-server"
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
