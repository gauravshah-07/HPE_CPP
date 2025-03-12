
import json
import time
import random
from datetime import datetime
from kafka import KafkaProducer

# Initialize Kafka producer
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8') 
)

def generate_random_data():
    return {
        "recordtimestamp": datetime.utcnow().isoformat() + "Z",
        "process_id": str(random.randint(100000, 999999)),
        "Attributes": {
            "priority": str(random.randint(1, 50)),  # Random priority
            "facility": str(random.randint(1, 10)), 
            "type": "log_syslog"
        },
        "Body": f"Connection closed by invalid user {random.choice(['alice', 'bob', 'charlie'])} {random.randint(100, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)} port {random.randint(40000, 60000)} [preauth]",
        "type": "log_syslog",
        "hostname": "cfhill",
        "priority": str(random.randint(1, 50)),   
        "facility": str(random.randint(1, 10)),
        "Resource": {
            "host.name": "cfhill",
            "service.name": "sshd",
            "process_id": str(random.randint(100000, 999999))
        },
        "Timestamp": datetime.utcnow().strftime("%b %d %H:%M:%S"),
        "Severity": random.choice(["info", "warning", "error"]),
        "identifier": "sshd"
    }

# Continuously send messages every 2 seconds
while True:
    data = generate_random_data()
    future = producer.send("myfirsttopic", data)
    
    try:
        record_metadata = future.get(timeout=10)  
        print(f"Message sent to {record_metadata.topic} at partition {record_metadata.partition}")
    except Exception as e:
        print(f"Error: {e}")

    producer.flush()
    time.sleep(2)  # Wait 2 seconds before sending the next message
