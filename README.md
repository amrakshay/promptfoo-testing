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

### **3. Setup MySQL**
Navigate to the MySQL setup folder:
```sh
cd mysql
```

The `init-db/` folder contains initial scripts for database creation.

Start the MySQL container:
```sh
./mysql.sh start
```
Once done, return to the main directory:
```sh
cd ..
```

---

### **4. Setup OpenSearch**
Navigate to the OpenSearch setup folder:
```sh
cd opensearch
```
Start the OpenSearch container:
```sh
./opensearch.sh start
```
Return to the main directory:
```sh
cd ..
```

---

### **5. Setup PAIG OpenSource Server**
Navigate to the PAIG OpenSource folder:
```sh
cd paig-opensource
```

(Optional) If you have a custom `.whl` file, remove the existing one and replace it:
```sh
rm paig_server-*.whl  # Remove existing wheel file
# Copy your own wheel file into this folder
```

Build the Docker image:
```sh
./build_image.sh
```

(Optional) Update the `.env` file to modify the default port (4545).

Start the PAIG OpenSource Server:
```sh
./paig-opensource-server.sh start
```

Access the UI at **[http://localhost:4545/login](http://localhost:4545/login)**

#### **Create Demo Data**
```sh
./paig-opensource-server.sh shell
cd /scripts/
python3 create_demo_data.py
exit
cd ..
```

Return to the main directory:
```sh
cd ..
```

---

### **6. Setup SecureChat Safe Server**
Navigate to the SecureChat Safe folder:
```sh
cd paig-securechat-safe
```

(Optional) Replace the existing wheel file with your own:
```sh
rm paig_securechat-*.whl
# Copy your wheel file here
```

Build the Docker image:
```sh
./build_image.sh
```

Download the shield config files:
```sh
docker run -v $(pwd)/scripts:/scripts -v $(pwd)/custom-configs:/custom-configs --network app-network --rm broadinstitute/python-requests "/scripts/download_shield_config_files.py"
```

(Optional) Update the `.env` file to modify the default port (5555).

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

### **7. Setup SecureChat Unsafe Server**
Navigate to the SecureChat Unsafe folder:
```sh
cd paig-securechat-unsafe
```

(Optional) Replace the existing wheel file with your own:
```sh
rm paig_securechat-*.whl
# Copy your wheel file here
```

Build the Docker image:
```sh
./build_image.sh
```

Download the shield config files:
```sh
docker run -v $(pwd)/scripts:/scripts -v $(pwd)/custom-configs:/custom-configs --network app-network --rm broadinstitute/python-requests "/scripts/download_shield_config_files.py"
```

(Optional) Update the `.env` file to modify the default port (6565).

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
