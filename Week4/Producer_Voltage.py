
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
        "MessageId": "CrayTelemetry.Voltage",
        "Timestamp": str(int(time.time() * 1000)),
        "Location": random.choice(['x9000c3r3b0', 'x9000c1r1b0', 'x9000c3r5b0', 'x9000c1r5b0', 'x9000c1r3b0', 'x9000c3r7b0', 'x3000c0r26b0', 'x9000c1r7b0', 'x9000c3r1b0']),
        "ParentalContext": {
            "string": random.choice(['ASIC', 'PowerSupplySubsystem', None])
        },
        "PhysicalContext": {
            "string": random.choice(['PowerSupply', 'VoltageRegulator', 'ASIC', 'NetworkingDevice'])
        },
        "PhysicalSubContext": {
            "string": random.choice(['Input', 'Output', None])
        },
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
    future = producer.produce("slingshot_CraySwitchHardwareTelemetry_voltage", value=str(data),callback=acked)
    producer.poll(1)
    producer.flush()
    time.sleep(2) 