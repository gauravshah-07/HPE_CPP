from confluent_kafka import Consumer
import signal
import json

running = True
def handle_sigint(sig, frame):
    global running
    running = False
    print("\n Stopping consumer...")

signal.signal(signal.SIGINT, handle_sigint)

def create_consumer():
    return Consumer({
        'bootstrap.servers': 'localhost:9092',
        'group.id': 'metric-consumer-group',
        'auto.offset.reset': 'earliest'
    })

def consume_messages(topics):
    consumer = create_consumer()
    consumer.subscribe(topics)
    print(f"Subscribed to topics: {topics}")

    try:
        while running:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                print(f"Consumer error: {msg.error()}")
                continue

            try:
                decoded = msg.value().decode('utf-8')
                try:
                    data = json.loads(decoded)
                    print(f"{msg.topic()} | JSON: {json.dumps(data, indent=2)}")
                except json.JSONDecodeError:
                    print(f"{msg.topic()} | Plain: {decoded}")
            except Exception as e:
                print(f"Error decoding message: {e}")
    finally:
        consumer.close()
        print("Consumer closed cleanly.")

if __name__ == "__main__":
    topics = ['SlurmSummary', 'Voltage']
    consume_messages(topics)
