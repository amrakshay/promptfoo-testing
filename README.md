# **PAIG Demo Environment Setup**

## **Table of Contents**
- [Prerequisites](#prerequisites)
- [Installation & Setup](#installation--setup)
  - [1. Clone the Repository](#1-clone-the-repository)
  - [2. Install Docker & Dependencies](#2-install-docker--dependencies)
  - [3. Setup MySQL](#3-setup-mysql)
  - [4. Setup OpenSearch](#4-setup-opensearch)
  - [5. Setup PAIG OpenSource Server](#5-setup-paig-opensource-server)
  - [6. Setup SecureChat Safe Server](#6-setup-securechat-safe-server)
  - [7. Setup SecureChat Unsafe Server](#7-setup-securechat-unsafe-server)
- [Teardown & Cleanup](#teardown--cleanup)

---

## **Prerequisites**
Before proceeding, ensure that you have the following installed:
- Linux-based OS (Tested on Amazon Linux)
- Git

---

## **Installation & Setup**

### **1. Clone the Repository**
```sh
git clone git@github.com:amrakshay/promptfoo-testing.git
cd promptfoo-testing
```

Set up the variable to refer to this directory:
```sh
export PAIG_DEMO_DIR=$(pwd)
```

### **2. Install Docker & Dependencies**
If Docker and Docker Compose are not installed, run:
```sh
./install_docker.sh
exit  # Restart the terminal
```
After restarting the terminal, navigate back to the project directory and run:
```sh
cd promptfoo-testing
./install_docker_compose.sh
./create_docker_network.sh  # Create a dedicated Docker network
```

---

### **3. Build PAIG Opensource Docker Image**
Navigate to the PAIG Opensource folder:
```sh
cd $PAIG_DEMO_DIR/docker-images/paig-opensource
```

<blockquote>
If you have a custom `.whl` file, You can copy your wheel file into this folder.

Make sure your wheel file follows naming convention as paig_server-${VERSION}-py3-none-any.whl.

For example, paig_server-0.1.0-py3-none-any.whl
</blockquote>

Build the Docker image:
```sh
./build_image.sh
```

### **4. Build PAIG Securechat Docker Image**
Navigate to the PAIG Securechat folder:
```sh
cd $PAIG_DEMO_DIR/docker-images/paig-securechat
```

<blockquote>
If you have a custom `.whl` file, You can copy your wheel file into this folder.

Make sure your wheel file follows naming convention as paig_securechat-${VERSION}-py3-none-any.whl.

For example, paig_securechat-0.1.0-py3-none-any.whl
</blockquote>

Build the Docker image:
```sh
./build_image.sh
```

### **5. Setup MySQL**
Navigate to the MySQL setup folder:
```sh
cd $PAIG_DEMO_DIR/mysql
```

The `init-db/` folder contains initial scripts for database creation.

Start the MySQL container:
```sh
./mysql.sh start
```

---

### **6. Setup OpenSearch**
Navigate to the OpenSearch setup folder:
```sh
cd $PAIG_DEMO_DIR/opensearch
```
Start the OpenSearch container:
```sh
./opensearch.sh start
```

---

### **7. Create Plant-Ops Data Index in Opensearch**
Navigate to the opensearch-plant-ops-index folder:
```sh
cd $PAIG_DEMO_DIR/external-data/opensearch-plant-ops-index
```

Copy the sample.env file to .env file and update the values:
```sh
cp sample.env .env
```

Run the script to create the index:
```sh
./create_index.sh
```

---

### **8. Setup PAIG OpenSource Server**
Navigate to the PAIG OpenSource folder:
```sh
cd $PAIG_DEMO_DIR/paig-opensource
```

Set up the `.env` file:
```sh
./paig-opensource-server.sh setup
```

Update the `.env` file 
- update your VERSION.
- add your OPENAI_API_KEY.

Start the PAIG OpenSource Server:
```sh
./paig-opensource-server.sh start
```

Access the UI at **[http://localhost:4545/login](http://localhost:4545/login)**

#### **Create Demo Data**
```sh
./paig-opensource-server.sh shell
```

```sh
cd /scripts/
python3 create_demo_data.py
```

Exit the shell:
```sh
exit
```

---

### **9. Setup SecureChat Safe Server**
Navigate to the SecureChat Safe folder:
```sh
cd $PAIG_DEMO_DIR/paig-securechat-safe
```

Set up the `.env` file:
```sh
./paig-opensource-server.sh setup
```

> Update the `.env` file to modify the default port (5555).

Download the shield config files:

Note:- If you have changed the paig server port in the .env file, then you need to update the port in the download_shield_config_files.py file as well under the scripts directory.
```sh
docker run -v $(pwd)/scripts:/scripts -v $(pwd)/custom-configs:/custom-configs --network app-network --rm broadinstitute/python-requests "/scripts/download_shield_config_files.py"
```

Start the SecureChat Safe Server:
```sh
./paig-securechat-server.sh start
```

Access the UI at **[http://localhost:5555/login](http://localhost:5555/login)**

#### **Check Logs (if needed)**
```sh
./paig-securechat-server.sh logs
```

Return to the main directory:
```sh
cd ..
```

---

### **10. Setup SecureChat Unsafe Server**
Navigate to the SecureChat Unsafe folder:
```sh
cd $PAIG_DEMO_DIR/paig-securechat-unsafe
```

Set up the `.env` file:
```sh
./paig-opensource-server.sh setup
```

> Update the `.env` file to modify the default port (5555).

Download the shield config files:

Note:- If you have changed the paig server port in the .env file, then you need to update the port in the download_shield_config_files.py file as well under the scripts directory.
```sh
docker run -v $(pwd)/scripts:/scripts -v $(pwd)/custom-configs:/custom-configs --network app-network --rm broadinstitute/python-requests "/scripts/download_shield_config_files.py"
```

Start the SecureChat Unsafe Server:
```sh
./paig-securechat-server.sh start
```

Access the UI at **[http://localhost:6565/login](http://localhost:6565/login)**

Return to the main directory:
```sh
cd ..
```

---

## **Teardown & Cleanup**
To stop and remove all running containers and clean up resources:
```sh
# Stop all running containers
docker stop $(docker ps -q)
```

Remove all containers:
```sh
docker rm $(docker ps -aq)
```

Remove all Docker images:
```sh
docker rmi $(docker images -q)
```

Remove Docker volume for OpenSearch:
```sh
docker volume rm opensearch_opensearch-data1
```

Remove the created Docker network:
```sh
docker network rm app-network
```

(Optional) Uninstall Docker:
```sh
sudo yum remove docker -y
```

---
