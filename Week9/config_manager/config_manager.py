import os
import yaml
import pickle
import hashlib
import argparse
from config_manager.prom_parser import PrometheusParser
from config_manager.json_parser import convert_file

CACHE_FILE = "cache_file.pkl"

def validate_yaml(data):
    if "filetype" not in data or "topic" not in data:
        raise ValueError("Missing required top-level fields.")
    for key, val in data.items():
        if key in ["filetype", "topic"]:
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
            except (EOFError, pickle.UnpicklingError) as e:
                print(f"Warning: Failed to load cache file ({e}). Starting with an empty cache.")
                return {}
            except Exception as e:
                print(f"Error: Unexpected issue while loading cache ({e}).")
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
        if isinstance(yaml_data, str) and os.path.exists(yaml_data):
            with open(yaml_data, 'r') as f:
                yaml_data = yaml.safe_load(f)
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
    prom_parser = subparsers.add_parser("prom2yaml", help="Prometheus file to YAML")
    prom_parser.add_argument('input_file', help='Path to the Prometheus file')
    prom_parser.add_argument('--topic',required=True, help='Topic name to include in YAML')
    prom_parser.add_argument('--output',required=False,help='Path to output YAML file')

    json_parser = subparsers.add_parser("json2yaml", help="Telemetry JSON to YAML summary")
    json_parser.add_argument("input_file", help="Path to the input JSON file")
    json_parser.add_argument("--metric_name",required=False, help="Metric name (e.g., 'pdu_input_power')")
    json_parser.add_argument("--topic", required=True,help="Topic (e.g., 'PDU Metrics')")
    json_parser.add_argument("--output",required=False, help="Path to the output YAML file")


    args = parser.parse_args()

    if args.command == "prom2yaml":
        if not args.output:
            args.output=f"{args.topic}.yaml"
        print("Parsing Prometheus file...")
        prom_parser = PrometheusParser(args.input_file, args.topic)
        yaml_data = prom_parser.parse()

    elif args.command == "json2yaml":
        if not args.output:
            args.output=f"{args.topic}.yaml"
        yaml_data = convert_file(args.input_file, args.output,args.metric_name,args.topic)


    try:
        validate_yaml(yaml_data)
        print("YAML validated successfully.")
    except Exception as e:
        print(f"Validation failed: {e}")
        return


    os.makedirs("YAML", exist_ok=True)

    output_path = os.path.join("YAML", os.path.basename(args.output))

    config_manager = ConfigManager()
    config = config_manager.get_config(yaml_data)

    with open(output_path, "w") as f:
        yaml.dump(config, f, sort_keys=False)

    print(f"YAML written to {output_path}")
    simulator_engine(config)


if __name__ == "__main__":
    main()





