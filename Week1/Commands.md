# Week-1 Commands Reference

#### Using Docker Compose:
```sh
docker compose -f docker-compose.yml up
```

#### Creating a Docker Network:
```sh
docker network create kafka-network
```

#### Start Zookeeper:
```sh
docker run -d --name zookeeper --network kafka-network -e ZOOKEEPER_CLIENT_PORT=2181 confluentinc/cp-zookeeper:latest
```

#### Start Kafka:
```sh
docker run -d --name kafka --network kafka-network -e KAFKA_ZOOKEEPER_CONNECT=zookeeper:2181 -e KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://localhost:9092 -e KAFKA_BROKER_ID=1 -e KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR=1 confluentinc/cp-kafka:latest
```

#### Create a Topic:
```sh
docker exec -it kafka kafka-topics --create --topic test-topic --partitions 1 --replication-factor 1 --if-not-exists --bootstrap-server localhost:9092
```

#### Send a Message:
```sh
docker exec -it kafka kafka-console-producer --broker-list localhost:9092 --topic test-topic
```

#### Consume the Message:
```sh
docker exec -it kafka kafka-console-consumer --bootstrap-server localhost:9092 --topic test-topic --from-beginning
```
