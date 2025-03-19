# Stop all running containers
docker stop $(docker ps -q)

docker rm $(docker ps -aq)

docker rmi $(docker images -q)

docker volume rm opensearch_opensearch-data1

docker network rm app-network

docker system prune -a -f