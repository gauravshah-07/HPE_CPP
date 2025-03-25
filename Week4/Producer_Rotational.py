
import json
import time
import random
from datetime import datetime
from confluent_kafka import Producer

import argparse

parser = argparse.ArgumentParser(description='Kafka Producer for CraySwitchHardwareTelemetry')
parser.add_argument('--bootstrap-server', default='admin:9092', help='Kafka bootstrap server address (default: admin:9092)')
args = parser.parse_args()


producer = Producer({"bootstrap.servers": args.bootstrap_server})

def generate_random_data():
    return {
        "TelemetrySource": "sC",
        "MessageId": "CrayTelemetry.Rotational",
        "Timestamp": str(int(time.time() * 1000)),
        "Location": random.choice(['x3000c0r26b0']),
        "ParentalContext": {
            "string": random.choice(['Chassis', 'PowerSupply'])
        },
        "PhysicalContext": {
            "string": random.choice(['Fan'])
        },
        "PhysicalSubContext": None,
        "ParentalIndex": None,
        "Index": {
            "int": str(random.randint(1, 10))
        },
        "DeviceSpecificContext": None,
        "Value": str(random.randint(5000, 15000))  # Adjust range as needed
    }
def acked(err, msg):
    if err is not None:
        print( "Failed to deliver message: %s: %s" % (str(msg), str(err)))
    else:
        print( "Message produced: %s"% (str(msg)))
# Continuously send messages every 2 seconds
while True:
    data = generate_random_data()
    future = producer.produce("slingshot_CraySwitchHardwareTelemetry_rotational", value=str(data),callback=acked)
    producer.poll(1)
    producer.flush()
    time.sleep(2) 