import json
from kafka import KafkaProducer
# Initialize Kafka producer
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8') 
)

data = {
    "recordtimestamp": "2025-02-27T08:07:36.000000000Z",
    "process_id": "1212173",
    "Attributes": {
        "priority": "38",
        "facility": "4",
        "type": "log_syslog"
    },
    "Body": "Connection closed by invalid user andya 128.162.236.150 port 48228 [preauth]",
    "type": "log_syslog",
    "hostname": "cfhill",
    "priority": "38",   
    "facility": "4",
    "Resource": {
        "host.name": "cfhill",
        "service.name": "sshd",
        "process_id": "1212173"
    },
    "Timestamp": "Feb 27 08:07:36",
    "Severity": "info",
    "identifier": "sshd"
}
# Send the message to the Kafka topic 'logs'
future = producer.send("logs", data)
try:
    record_metadata = future.get(timeout=10)  
    print(f" Message sent to {record_metadata.topic} at partition {record_metadata.partition}")
except Exception as e:
    print(f" Error: {e}")
# Ensure all messages are sent before closing the producer
producer.flush()
