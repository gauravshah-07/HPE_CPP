# After adding option for showing list of all topics

import argparse
import os
import yaml
from config_manager.config_manager import ConfigManager, validate_yaml, simulator_engine
from simulator.simulator import MetricSimulator
from producer.Producer import main as producer_main
from config_manager.prom_parser import PrometheusParser
from config_manager.json_parser import convert_file
import ast
CONFIG_DIR = "YAML"
KAFKA_CONFIG_PATH = "kafka_config.yaml"
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
    def generate(self, topic_name, value_ranges=None):
        try:
            path = os.path.join(CONFIG_DIR, f"{topic_name}.yaml")
            if not os.path.exists(path):
                raise FileNotFoundError(f"YAML config '{topic_name}.yaml' not found in {CONFIG_DIR}.")
            sim = MetricSimulator(path)
            print("Sample metric:")
            sim.simulate_metrics(value_ranges=value_ranges)
        except Exception as e:
            print(f"Error: {e}")

class KafkaProducerCLI:
    def __init__(self):
        self.bootstrap_server = "admin:9092"
        self.load_config()

    def load_config(self):
        if os.path.exists(KAFKA_CONFIG_PATH):
            with open(KAFKA_CONFIG_PATH, "r") as f:
                data = yaml.safe_load(f)
                if data and "bootstrap_server" in data:
                    self.bootstrap_server = data["bootstrap_server"]

    def save_config(self):
        with open(KAFKA_CONFIG_PATH, "w") as f:
            yaml.dump({"bootstrap_server": self.bootstrap_server}, f)

    def configure(self, server: str):
        self.bootstrap_server = server
        self.save_config()
        print(f"Kafka server set to: {self.bootstrap_server}")

    def run(self, *topics, value_ranges=None):
        if isinstance(value_ranges, str):
            try:
                value_list = ast.literal_eval(value_ranges)
                value_ranges = [(str(value_list[0]), str(value_list[1]))]
            except Exception:
                print("No input or Invalid input type. Using values from yaml.")
                value_ranges = None
        try:
            config_paths = []
            for topic in topics:
                path = os.path.join(CONFIG_DIR, f"{topic}.yaml")
                if not os.path.exists(path):
                    raise FileNotFoundError(f"Config file for topic '{topic}' not found.")
                config_paths.append(path)

            os.environ['KAFKA_BOOTSTRAP_SERVER'] = self.bootstrap_server
            producer_main(config_paths, value_ranges=value_ranges)

        except Exception as e:
            print(f"Error: {e}")

class CLIApp:
    def __init__(self):
        self.topic = TopicManager()
        self.simulate = SampleSimulator()
        self.producer = KafkaProducerCLI()
    def list_topics(self):
        try:
            if not os.path.exists(CONFIG_DIR):
                print("No topics found. 'YAML/' directory does not exist.")
                return
            topics = [f[:-5] for f in os.listdir(CONFIG_DIR) if f.endswith('.yaml')]
            if topics:
                print("\nAvailable Topics:")
                print("-----------------")
                for topic in topics:
                    print(f"- {topic}")
            else:
                print("No topic YAML files found in the YAML/ directory.")
        except Exception as e:
            print(f"Error: {e}")
            
    def menu(self):
        while True:
            print("\nCLI MENU")
            print("------------------------")
            print("1. Create")
            print("2. Produce")
            print("3. Validate")
            print("4. List")
            print("5. Exit")
            choice = input("Enter choice: ").strip()

            if choice == "1":
                file_type = input("Enter file type (prom/json): ").strip().lower()
                input_file = input("Enter path to input file: ").strip()
                topic = input("Enter topic name: ").strip()

                if file_type == "prom":
                    self.topic.prom2yaml(input_file, topic)
                elif file_type == "json":
                    metric = input("Metric name (optional): ").strip() or None
                    self.topic.json2yaml(input_file, topic, metric)
                else:
                    print("Invalid file type. Please enter 'prom' or 'json'.")

            elif choice == "2":
                self.producer_menu()

            elif choice == "3":
                self.list_topics()
                topic = input("Enter topic name to validate: ").strip()
                path = os.path.join(CONFIG_DIR, f"{topic}.yaml")
                if os.path.exists(path):
                    try:
                        with open(path) as f:
                            config = yaml.safe_load(f)
                            validate_yaml(config)
                            print("YAML validation successful.")
                    except Exception as e:
                        print(f"Validation failed: {e}")
                else:
                    print(f"No YAML found for topic '{topic}'")

            elif choice == "4":
                self.list_topics()

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
                self.list_topics()
                topics = input("Enter topic names (comma-separated): ").split(",")
                topics = [t.strip() for t in topics]
                ranges_input = input("Enter value ranges as a list (e.g. [10,20]): ")

                try:
                    value_list = ast.literal_eval(ranges_input)
                    value_ranges = [(str(value_list[0]), str(value_list[1]))]
                except Exception:
                    print("No input or Invalid format for value ranges. Using values from yaml.")
                    value_ranges = None
                self.producer.run(*topics,value_ranges=value_ranges)

            elif subchoice == "3":
                break
            else:
                print("Invalid choice")
def main():
    app = CLIApp()
    parser = argparse.ArgumentParser(description="CLI for managing topics, simulating metrics, and producing to Kafka.")
    subparsers = parser.add_subparsers(dest='command')

    # Prometheus to YAML
    prom_parser = subparsers.add_parser('prom2yaml', help='Convert Prometheus file to YAML')
    prom_parser.add_argument('input_file', help='Path to Prometheus input file')
    prom_parser.add_argument('topic', help='Topic name')

    # JSON to YAML
    json_parser = subparsers.add_parser('json2yaml', help='Convert JSON file to YAML')
    json_parser.add_argument('input_file', help='Path to JSON input file')
    json_parser.add_argument('topic', help='Topic name')


    # Generate sample metric
    generate_parser = subparsers.add_parser('generate', help='Generate sample metric')
    generate_parser.add_argument('topic_name', help='Topic name')
    generate_parser.add_argument('--value_ranges', type=str, help="Value ranges as a list, e.g. [10,20]")

    # Kafka producer config
    config_parser = subparsers.add_parser('configure', help='Configure Kafka broker')
    config_parser.add_argument('server', help='Kafka bootstrap server')

    # Kafka producer run
    run_parser = subparsers.add_parser('run', help='Run Kafka producer')
    run_parser.add_argument('topics', nargs='+', help='Topic names to produce to')
    run_parser.add_argument('--value_ranges', type=str, help="Value ranges as a list, e.g. [10,20]")
    list_parser = subparsers.add_parser('list-topics', help='List all available topics')

    #prom to Producer
    prom2produce_parser = subparsers.add_parser('prom2produce', help='Convert Prometheus to YAML, simulate, and produce to Kafka')
    prom2produce_parser.add_argument('input_file')
    prom2produce_parser.add_argument('topic', nargs='+', help='Topic names to produce to')
    prom2produce_parser.add_argument('--value_ranges', type=str, help="Value ranges as a list, e.g. [10,20]")

    #json to Producer
    json2produce_parser = subparsers.add_parser('json2produce', help='Convert JSON to YAML, simulate, and produce to Kafka')
    json2produce_parser.add_argument('input_file')
    json2produce_parser.add_argument('topic', nargs='+', help='Topic names to produce to')
    json2produce_parser.add_argument('--value_ranges', type=str, help="Value ranges as a list, e.g. [10,20]")



    it_parser = subparsers.add_parser('i', help='Run Interactive Mode')
    args = parser.parse_args()

    if args.command == 'prom2yaml':
        app.topic.prom2yaml(args.input_file, args.topic)
    elif args.command == 'json2yaml':
        app.topic.json2yaml(args.input_file, args.topic, args.metric_name)
    elif args.command == 'generate':
        app.simulate.generate(args.topic_name)
    elif args.command == 'configure':
        app.producer.configure(args.server)
    elif args.command == 'run':
        app.producer.run(*args.topics, value_ranges=args.value_ranges)
    elif args.command == 'list-topics':
        app.list_topics()
    elif args.command == 'prom2produce':
        app.topic.prom2yaml(args.input_file, args.topic)
        app.simulate.generate(args.topic)
        app.producer.run(args.topic, value_ranges=args.value_ranges)

    elif args.command == 'json2produce':
        app.topic.json2yaml(args.input_file, args.topic, args.metric_name)
        app.simulate.generate(args.topicrun_parser.add_argument('--value_ranges', type=str, help="Value ranges as a list, e.g. [10,20]"))
        app.producer.run(args.topic, value_ranges=args.value_ranges)

    elif args.command == 'i':
        app.menu()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
