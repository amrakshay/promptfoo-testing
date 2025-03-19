
# Set the version of the PAIG components
export PAIG_OPENSOURCE_VERSION=0.0.6
export PAIG_SECURECHAT_VERSION=0.0.3

# Create a dedicated Docker network for the PAIG components
./create_docker_network.sh

# Set the PAIG_DEMO_DIR environment variable
export PAIG_DEMO_DIR=$(pwd)

# Build PAIG Open Source Docker image
cd $PAIG_DEMO_DIR/docker-images/paig-opensource
./build_image.sh

# Build PAIG Secure Chat Docker image
cd $PAIG_DEMO_DIR/docker-images/paig-securechat
./build_image.sh

# Setup MySQL database
cd $PAIG_DEMO_DIR/dockers/mysql
./mysql.sh start

# Sleep for 5 seconds to allow the MySQL database to start
echo "Sleeping for 5 seconds to allow the MySQL database to start..."
sleep 5

# Setup OpenSearch
cd $PAIG_DEMO_DIR/dockers/opensearch
./opensearch.sh start

# Sleep for 5 seconds to allow the OpenSearch to start
echo "Sleeping for 5 seconds to allow the OpenSearch to start..."
sleep 5

# Create Plant-Ops Data Index in Opensearch
cd $PAIG_DEMO_DIR/external-data/opensearch-plant-ops-index
cp sample.env .env
./create_index.sh

# Setup PAIG Open Source Server
cd $PAIG_DEMO_DIR/dockers/paig-opensource
./paig-opensource-server.sh setup

read -p "Please provide your OPENAI_API_KEY: " OPENAI_API_KEY
sed -i "s/^OPENAI_API_KEY=.*/OPENAI_API_KEY=${OPENAI_API_KEY}/" .env

./paig-opensource-server.sh start

# Sleep for 30 seconds to allow the PAIG Open Source Server to start
echo "Sleeping for 30 seconds to allow the PAIG Open Source Server to start..."
sleep 30

# Asking user to access the PAIG Open Source Server on the browser http://localhost:4545
echo "Please access the PAIG Open Source Server on the browser http://localhost:4545 and login with the following credentials then press enter to continue..."

read -p "Press enter to continue..."

# Create Demo Data in PAIG Server
./paig-opensource-server.sh create-demo-data

# Setup PAIG SecureChat Safe Server
cd $PAIG_DEMO_DIR/dockers/paig-securechat-safe
./paig-securechat-server.sh setup
docker run -v $(pwd)/scripts:/scripts -v $(pwd)/custom-configs:/custom-configs --network app-network --rm broadinstitute/python-requests "/scripts/download_shield_config_files.py"
./paig-securechat-server.sh start

# Sleep for 60 seconds to allow the PAIG Secure Safe Server to start
echo "Sleeping for 60 seconds to allow the PAIG Secure Safe Server to start..."
sleep 60

# Setup PAIG SecureChat Unsafe Server
cd $PAIG_DEMO_DIR/dockers/paig-securechat-unsafe
./paig-securechat-server.sh setup
docker run -v $(pwd)/scripts:/scripts -v $(pwd)/custom-configs:/custom-configs --network app-network --rm broadinstitute/python-requests "/scripts/download_shield_config_files.py"
./paig-securechat-server.sh start

# Sleep for 30 seconds to allow the PAIG Secure Unsafe Server to start
echo "Sleeping for 30 seconds to allow the PAIG Secure Unsafe Server to start..."
sleep 30

echo "Setup complete!"
