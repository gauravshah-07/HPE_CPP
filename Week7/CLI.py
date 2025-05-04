import fire
import os
import yaml
from config_manager import ConfigManager, validate_yaml, simulator_engine
from simulator import MetricSimulator
from Producer import main as producer_main
from prom_parser import PrometheusParser
from json_parser import convert_file

CONFIG_DIR = "YAML"
CACHE = ConfigManager()

class TopicManager:
    def prom2yaml(self, input_file, topic, output=None):
        try:
            if not os.path.exists(input_file):
                raise FileNotFoundError(f"File '{input_file}' not found.")
            if not output:
                output = f"{topic}.yaml"

            parser = PrometheusParser(input_file, topic)
            yaml_data = parser.parse()
            validate_yaml(yaml_data)

            os.makedirs(CONFIG_DIR, exist_ok=True)
            path = os.path.join(CONFIG_DIR, os.path.basename(output))
            config = CACHE.get_config(yaml_data)

            with open(path, "w") as f:
                yaml.dump(config, f, sort_keys=False)
            print(f"YAML written to {path}")
            simulator_engine(config)

        except Exception as e:
            print(f"Error: {e}")

    def json2yaml(self, input_file, topic, metric_name=None, output=None):
        try:
            if not os.path.exists(input_file):
                raise FileNotFoundError(f"File '{input_file}' not found.")
            if not output:
                output = f"{topic}.yaml"

            yaml_data = convert_file(input_file, output, metric_name, topic)
            validate_yaml(yaml_data)

            os.makedirs(CONFIG_DIR, exist_ok=True)
            path = os.path.join(CONFIG_DIR, os.path.basename(output))
            config = CACHE.get_config(yaml_data)

            with open(path, "w") as f:
                yaml.dump(config, f, sort_keys=False)
            print(f"YAML written to {path}")
            simulator_engine(config)

        except Exception as e:
            print(f"Error: {e}")

class SampleSimulator:
    def generate(self, topic_name):
        try:
            path = os.path.join(CONFIG_DIR, f"{topic_name}.yaml")
            if not os.path.exists(path):
                raise FileNotFoundError(f"YAML config '{topic_name}.yaml' not found in {CONFIG_DIR}.")
            sim = MetricSimulator(path)
            print("Sample metric:")
            sim.simulate_metrics()
        except Exception as e:
            print(f"Error: {e}")

class KafkaProducerCLI:
    def __init__(self):
        self.bootstrap_server = "admin:9092"

    def configure(self, server: str):
        self.bootstrap_server = server
        print(f"Kafka server set to: {self.bootstrap_server}")

    def run(self, *topics):
        try:
            config_paths = []
            for topic in topics:
                path = os.path.join(CONFIG_DIR, f"{topic}.yaml")
                if not os.path.exists(path):
                    raise FileNotFoundError(f"Config file for topic '{topic}' not found.")
                config_paths.append(path)

            os.environ['KAFKA_BOOTSTRAP_SERVER'] = self.bootstrap_server
            producer_main(config_paths)

        except Exception as e:
            print(f"Error: {e}")

class CLIApp:
    def __init__(self):
        self.topic = TopicManager()
        self.simulate = SampleSimulator()
        self.producer = KafkaProducerCLI()

    def menu(self):
        while True:
            print("\nCLI MENU")
            print("------------------------")
            print("1. Create YAML from Prometheus")
            print("2. Create YAML from JSON")
            print("3. Generate one sample data from topic")
            print("4. Kafka Producer Menu")
            print("5. Exit")
            choice = input("Enter choice: ").strip()

            if choice == "1":
                input_file = input("Enter path to Prometheus file: ")
                topic = input("Enter topic name: ")
                self.topic.prom2yaml(input_file, topic)

            elif choice == "2":
                input_file = input("Enter path to JSON file: ")
                topic = input("Enter topic name: ")
                metric = input("Metric name (optional): ").strip() or None
                self.topic.json2yaml(input_file, topic, metric)

            elif choice == "3":
                topic = input("Enter topic name: ")
                self.simulate.generate(topic)

            elif choice == "4":
                self.producer_menu()

            elif choice == "5":
                print("Exiting.")
                break
            else:
                print("Invalid choice")

    def producer_menu(self):
        while True:
            print("\nPRODUCER MENU")
            print("------------------------")
            print("1. Configure Kafka broker")
            print("2. Run producer for topics")
            print("3. Back to main menu")
            subchoice = input("Enter choice: ").strip()

            if subchoice == "1":
                server = input("Enter Kafka broker (e.g. localhost:9092): ")
                self.producer.configure(server)

            elif subchoice == "2":
                topics = input("Enter topic names (comma-separated): ").split(",")
                topics = [t.strip() for t in topics]
                self.producer.run(*topics)

            elif subchoice == "3":
                break
            else:
                print("Invalid choice")

if __name__ == "__main__":
    app = CLIApp()
    if len(os.sys.argv) == 1:
        app.menu()
    else:
        fire.Fire(app)
