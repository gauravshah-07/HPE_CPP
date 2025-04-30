## 1. Clone this repository
## 2. Run Confluent Kafka docker container
```bash
docker-compose up -d
```
## 3.Install dependencies
```bash
pip install confluent_kafka pyyaml
```
## 4. Create kafka topics within docker container
```bash
docker exec -it broker bash
```
```bash
kafka-topics --bootstrap-server localhost:29092 --create --topic PDUMetrics --replication-factor 1
kafka-topics --bootstrap-server localhost:29092 --create --topic TelemetryMetrics --replication-factor 1
```
## 5.Run the Producer
```bash
python producer.py config1.yaml config2.yaml
```
Here, the sample yaml files considered are json_sample.yaml and prom_sample.yaml which are attached with the files above

## 6.Run the consumer
```bash
python consumer.py
```
## 7. Stop the container
```bash
docker-compose down
```
