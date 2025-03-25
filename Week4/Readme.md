# Kafka Producer Setup Guide

This guide will help you set up and run the Kafka producer system using Docker and Docker Compose. Follow the steps below to clone the repository, build the containers, and start the producer scripts.

### 1. Clone the Repository

Run the following command to clone the repository and navigate to the required folder:

```sh
git clone --depth 1 --filter=blob:none --sparse https://github.com/prince-jain0/hpe-cpp.git
cd hpe-cpp
git sparse-checkout set Week4
cd Week4
```

### 2. Build the Docker Containers

Use Docker Compose to build the required images:

```sh
docker-compose build
```

### 3. Start the Kafka Producer System

Run the following command to start the services:

```sh
docker-compose up -d
```

This will start all the required services in detached mode.

### 4. Running a Producer Script

To run a specific producer script inside the container, use the following command:

```sh
docker exec -it kafka_producer bash -c 'echo "2" | python run.py --bootstrap-server admin:9092'
```

- The `echo "2"` simulates a user selecting an option from the menu.
- You can change the number to select different producer scripts.
- You can also modify the bootstrap-server address.

### 5. Stopping the System

To stop and remove all running containers, use:

```sh
docker-compose down
```


