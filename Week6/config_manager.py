import os
import re
import yaml
import pickle
import hashlib
import argparse
from datetime import datetime
from collections import defaultdict
from prom_parser import PrometheusParser
from json_parser import convert_file

CACHE_FILE = "cache_file.pkl"

def validate_yaml(data):
    if "FileType" not in data or "Topic" not in data:
        raise ValueError("Missing required top-level fields.")
    for key, val in data.items():
        if key in ["FileType", "Topic"]:
            continue
        if "labels" not in val or "value" not in val or "timestamp" not in val:
            raise ValueError(f"Missing fields in metric {key}")
    return True

class ConfigManager:
    def __init__(self, cache_file=CACHE_FILE):
        self.cache_file = cache_file
        self.cache = self.load_cache()

    def load_cache(self):
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, "rb") as f:
                    return pickle.load(f)
            except EOFError:
                return {}
        return {}

    def save_cache(self):
        with open(self.cache_file, "wb") as f:
            pickle.dump(self.cache, f)

    def generate_hash(self, yaml_data):
        yaml_str = yaml.dump(yaml_data, sort_keys=True)
        return hashlib.sha256(yaml_str.encode()).hexdigest()

    def is_cached(self, yaml_data):
        return self.generate_hash(yaml_data) in self.cache

    def add_to_cache(self, yaml_data):
        data_hash = self.generate_hash(yaml_data)
        self.cache[data_hash] = yaml_data
        self.save_cache()

    def get_config(self, yaml_data):
        if self.is_cached(yaml_data):
            print("Config already cached. Reusing schema...")
            return self.cache[self.generate_hash(yaml_data)]
        else:
            print("New config detected. Caching and passing to simulation.")
            self.add_to_cache(yaml_data)
            return yaml_data

def simulator_engine(yaml_config):
    print("\nRunning simulation with the following config:\n")
    print(yaml.dump(yaml_config, sort_keys=False, default_flow_style=False))


def main():
    parser = argparse.ArgumentParser(description="Telemetry & Prometheus YAML generator")

    subparsers = parser.add_subparsers(dest="command", required=True)

    # Subparser for Prometheus
    prom_parser = subparsers.add_parser("prom2yaml", help="Prometheus file to YAML")
    prom_parser.add_argument('--file', required=True, help='Path to the Prometheus file')
    prom_parser.add_argument('--topic', required=True, help='Topic name to include in YAML')
    prom_parser.add_argument('--output', default='output_simulator_ready.yaml', help='Path to output YAML file')

    # Subparser for JSON telemetry
    json_parser = subparsers.add_parser("json2yaml", help="Telemetry JSON to YAML summary")
    json_parser.add_argument("input_file", help="Path to the input JSON file")
    json_parser.add_argument("output", help="Path to the output YAML file")
    json_parser.add_argument("metric_name", help="Metric name (e.g., 'pdu_input_power')")
    json_parser.add_argument("topic", help="Topic (e.g., 'PDU Metrics')")

    args = parser.parse_args()

    if args.command == "prom2yaml":
        print("Parsing Prometheus file...")
        prom_parser = PrometheusParser(args.file, args.topic)
        yaml_data = prom_parser.parse()

    elif args.command == "json2yaml":
        yaml_data = convert_file(args.input_file, args.output, args.metric_name,args.topic)


    try:
        validate_yaml(yaml_data)
        print("YAML validated successfully.")
    except Exception as e:
        print(f"Validation failed: {e}")
        return

    config_manager = ConfigManager()
    config = config_manager.get_config(yaml_data)
    with open(args.output, "w") as f:
        yaml.dump(config, f, sort_keys=False)

    print(f"YAML written to {args.output}")
    simulator_engine(config)

if __name__ == "__main__":
    main()






