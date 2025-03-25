import json
import time
import random
from datetime import datetime,timezone
from confluent_kafka import Producer

import argparse

parser = argparse.ArgumentParser(description='Kafka Producer for CraySwitchHardwareTelemetry')
parser.add_argument('--bootstrap-server', default='admin:9092', help='Kafka bootstrap server address (default: admin:9092)')
args = parser.parse_args()


producer = Producer({"bootstrap.servers": args.bootstrap_server})
PARENTAL_CONTEXT_LIST = ["ASIC", "PowerSupplySubsystem", None]
PHYSICAL_SUB_CONTEXT_LIST = ["Output", "Input"]
PARENTAL_INDEX_LIST = [None]
def generate_random_data():
    return {
         "TelemetrySource": "sC",
        "MessageId": "CrayTelemetry.Power",
        "Timestamp": int(datetime.now(timezone.utc).timestamp() * 1000),  
        "Location": random.choice(['x9000c3r3b0', 'x9000c1r1b0', 'x9000c3r5b0', 'x9000c1r5b0', 'x9000c1r3b0', 'x9000c3r7b0', 'x3000c0r26b0', 'x9000c1r7b0', 'x9000c3r1b0']),
        "ParentalContext": {"string": random.choice(PARENTAL_CONTEXT_LIST)},
        "PhysicalContext": {"string": "VoltageRegulator"},
        "PhysicalSubContext": {"string": random.choice(PHYSICAL_SUB_CONTEXT_LIST)},
        "ParentalIndex": random.choice(PARENTAL_INDEX_LIST),
        "Index": {"int": random.randint(1, 100)},
        "DeviceSpecificContext": None,
        "Value": random.randint(1, 200) 
    }
def acked(err, msg):
    if err is not None:
        print( "Failed to deliver message: %s: %s" % (str(msg), str(err)))
    else:
        print( "Message produced: %s"% (str(msg)))
# Continuously send messages every 2 seconds
while True:
    data = generate_random_data()
    future = producer.produce("slingshot_CraySwitchHardwareTelemetry_power", value=str(data),callback=acked)
    producer.poll(1)
    producer.flush()
    time.sleep(2) 