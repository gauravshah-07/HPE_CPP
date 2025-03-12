from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    "myfirsttopic",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    group_id="consumer-group-1",
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
)

print("Waiting for messages...")

for message in consumer:
    print(f"Received: {message.value}")
