import json
import random
import time
from confluent_kafka import Producer
import argparse

parser = argparse.ArgumentParser(description='Kafka Producer for CraySwitchHardwareTelemetry')
parser.add_argument('--bootstrap-server', default='admin:9092', help='Kafka bootstrap server address (default: admin:9092)')
args = parser.parse_args()


producer = Producer({"bootstrap.servers": args.bootstrap_server})

locations = ['x9000c3r1b0', 'x3000c0r26b0', 'x9000c3r5b0', 'x9000c3r3b0', 
             'x9000c1r5b0', 'x9000c1r3b0', 'x9000c1r1b0', 'x9000c1r7b0', 'x9000c3r7b0']

parental_contexts = ['PowerSupplySubsystem', 'ASIC']
physical_contexts = ['VoltageRegulator', 'PowerSupply'] 
physical_sub_contexts = ['Output', 'Input']

def generate_random_data():
    return {
        "TelemetrySource": "sC",
        "MessageId": "CrayTelemetry.Current",
        "Timestamp": int(time.time() * 1000),  
        "Location": random.choice(locations),
        "ParentalContext": {"string": random.choice(parental_contexts)},
        "PhysicalContext": {"string": random.choice(physical_contexts)},
        "PhysicalSubContext": {"string": random.choice(physical_sub_contexts)},
        "ParentalIndex": None,
        "Index": {"int": random.randint(0, 10)},  
        "DeviceSpecificContext": None,
        "Value": round(random.uniform(0, 100), 3)  
    }

def acked(err, msg):
    if err is not None:
        print("Failed to deliver message: %s: %s" % (str(msg), str(err)))
    else:
        # Print the actual message value
        print("Message produced: %s" % (msg.value().decode('utf-8')))


while True:
    data = generate_random_data()
    future = producer.produce("slingshot_CraySwitchHardwareTelemetry_current",
                              value=json.dumps(data),  # Convert to JSON string
                              callback=acked)
    producer.poll(1)
    producer.flush()
    time.sleep(2)
