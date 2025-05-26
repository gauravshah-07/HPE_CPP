import threading
import time
import json
import sys
import queue
from confluent_kafka import Producer
from simulator.simulator import MetricSimulator  
import os
message_queue = queue.Queue()
shutdown_event = threading.Event()
def delivery_report(err, msg):
    if err is not None:
        print(f"Delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

def producer_worker(producer):
    while not shutdown_event.is_set():
        try:
            topic, message = message_queue.get(timeout=1)
            producer.produce(topic=topic, value=message.encode('utf-8'), callback=delivery_report)
            producer.poll(0)
            message_queue.task_done()
        except queue.Empty:
            continue
        except BufferError:
            print("Kafka buffer full. Retrying...")
            time.sleep(0.5)
        except Exception as e:
            print(f" Kafka error: {e}")

def simulator_thread(simulator: MetricSimulator, interval: float = 2.0,value_ranges=None):
    topic = simulator.getTopic()
    while not shutdown_event.is_set():
        try:
            print("Topic Produced:",topic)
            metrics = simulator.simulate_metrics(value_ranges=value_ranges)
            for metric, filetype in metrics:
                if filetype == "json":
                    message = json.dumps(metric)
                else:
                    message = str(metric)
                message_queue.put((topic, message))
            time.sleep(interval)
        except Exception as e:
            print(f"Error in simulator thread for topic '{topic}': {e}")
            time.sleep(interval)

def main(config_files,value_ranges=None):

    kafka_conf = {
        'bootstrap.servers':  os.getenv("KAFKA_BOOTSTRAP_SERVER", 'localhost:9092'),
        'linger.ms': 5,
        'compression.type': 'lz4',
        'batch.num.messages': 1000
    }
    producer = Producer(kafka_conf)
    threading.Thread(target=producer_worker, args=(producer,), daemon=True).start()
    for cfg_path in config_files:
        try:
            sim = MetricSimulator(cfg_path)
            threading.Thread(target=simulator_thread, args=(sim,2.0, value_ranges), daemon=True).start()
            print(f"Simulator started for topic: {sim.getTopic()} ({cfg_path})")
        except Exception as e:
            print(f"Failed to start simulator for {cfg_path}: {e}")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nExiting... Signaling threads to stop.")
        shutdown_event.set()
        time.sleep(2)  
        print("Flushing Kafka producer.")
        producer.flush()
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python Producer.py <config1.yaml> <config2.yaml> ...")
    else:
        config_files = sys.argv[1:]
        main(config_files)