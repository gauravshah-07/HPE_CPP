# Week-2 Challenges Faced:
#### Resolved Issues:
1. Same content sent again was ignored by Kafka, so `enable_auto_commit` was used to ensure messages were consumed properly.
2. Kafka wouldn't work due to port `9092` being blocked by the firewall. Resolved by allowing the port through the firewall settings.
3. A folder was created to store the syslogs received on the consumer end.
4. Resolved Kafka topic persistence issue by setting a volume parameter in docker-compose.yaml to retain data after container restarts.
5. Kafka AdminClient failed to connect to localhost:9902; resolved by fixing advertised listeners, ensuring broker availability, and restarting Kafka & Zookeeper.
6. Kafka failed to start due to a `cluster.id` mismatch in `/bitnami/kafka/data/meta.properties`; resolved by adding a volume to Zookeeper to persist metadata.
#### Open Issues:
##### (None)
