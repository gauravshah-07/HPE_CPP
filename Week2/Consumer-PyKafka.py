import json
from kafka import KafkaConsumer
# Initialize Kafka consumer to listen to the 'logs' topic
consumer = KafkaConsumer(
    "logs",
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest', 
    enable_auto_commit=False,   #Disable auto-commit to manually control message offsets
    group_id="my-group", 
    value_deserializer=lambda v: json.loads(v.decode('utf-8')) if v else None
)

print(" Waiting for messages...")
# Continuously listen for incoming messages
for message in consumer:
    if message.value:
        print(" Received message:", json.dumps(message.value, indent=4))
    else:
        print(" Skipping empty message")
