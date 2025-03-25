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
        "MessageId": "CrayTelemetry.Temperature",
        "Timestamp": int(time.time() * 1000),
        "Location": random.choice([
            "x9000c1r5b0",
            "x9000c3r7b0",
            "x9000c1r1b0",
            "x9000c3r1b0",
            "x9000c1r3b0",
            "x3000c0r26b0",
            "x9000c1r7b0",
            "x9000c3r5b0",
            "x9000c3r3b0"
        ]),
        "ParentalContext": random.choice([{"string": "ASIC"}, {"string": "SystemBoard"}, None]),
        "PhysicalContext": {
            "string": random.choice(['VoltageRegulator', 'NetworkingDevice', 'SystemBoard', 'ASIC','PowerSupply'])
        },
        "PhysicalSubContext": None,
        "ParentalIndex": None,
        "Index": {
            "int": random.randint(1, 10)
        },
        "DeviceSpecificContext": None,
        "Value": random.randint(29, 46)
    }

def acked(err, msg):
    if err is not None:
        print( "Failed to deliver message: %s: %s" % (str(msg), str(err)))
    else:
        print( "Message produced: %s"% (str(msg)))
while True:
    data = generate_random_data()
    future = producer.produce("slingshot_CraySwitchHardwareTelemetry_temperature", value=str(data),callback=acked)
    producer.poll(1)
    producer.flush()
    time.sleep(2) 