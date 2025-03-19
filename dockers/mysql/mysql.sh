STATE=${1}

if [[ $STATE == "start" ]]
then
  echo "Starting mysql"
  docker-compose up -d
elif [[ $STATE == "stop" ]]
then
  echo "Stopping mysql"
  docker-compose down
elif [[ $STATE == "mysql" ]]
then
  docker exec -it mysql-container mysql -u root -p
elif [[ $STATE == "logs" ]]
then
  docker logs -f mysql-container
elif [[ $STATE == "shell" ]]
then
  docker exec -it mysql-container bash
fi
