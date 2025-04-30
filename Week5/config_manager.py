import os
import re
import yaml
import pickle
import hashlib
from datetime import datetime
from collections import defaultdict
from prom_parser import PrometheusParser

CACHE_FILE = "cache_file.pkl"
PROM_FILE = "metrics_pdu.txt"
OUTPUT_YAML = "output_simulator_ready.yaml"


def parse_prometheus_file(file_path):
    with open(file_path, "r") as f:
        lines = f.readlines()

    pattern = re.compile(r'(\w+)\{([^}]*)\}\s+([\d.]+)\s+([\d.]+)')
    output_data = {
        "FileType": "prom",
        "Topic": "PDU_Metrics"
    }

    metric_store = {}

    for line in lines:
        match = pattern.match(line)
        if not match:
            continue

        metric, labels_str, value_str, timestamp_str = match.groups()
        value = float(value_str)

        # Parse labels
        labels_dict = dict(kv.split('=') for kv in labels_str.split(','))
        labels_dict = {k: v.strip('"') for k, v in labels_dict.items()}

        if metric not in metric_store:
            metric_store[metric] = {
                "labels": defaultdict(set),
                "values": [],
                "timestamp": int(float(timestamp_str))
            }

        for k, v in labels_dict.items():
            metric_store[metric]["labels"][k].add(v)

        metric_store[metric]["values"].append(value)

    for metric, data in metric_store.items():
        # Compute value range
        min_val = min(data["values"])
        max_val = max(data["values"])
        # Format labels
        formatted_labels = [{k: sorted(list(v))} for k, v in data["labels"].items()]
        output_data[metric] = {
            "labels": formatted_labels,
            "value": [f"({min_val}, {max_val})"],
            "timestamp": data["timestamp"]
        }

    return output_data


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
                # Handle the case where the file is empty
                return {}
        return {}


    def save_cache(self):
        with open(self.cache_file, "wb") as f:
            pickle.dump(self.cache, f)

    def generate_hash(self, yaml_data):
        yaml_str = yaml.dump(yaml_data, sort_keys=True)
        return hashlib.sha256(yaml_str.encode()).hexdigest()

    def is_cached(self, yaml_data):
        data_hash = self.generate_hash(yaml_data)
        return data_hash in self.cache

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
    print(" Parsing Prometheus file...")
    parser = PrometheusParser(PROM_FILE)
    yaml_data = parser.parse()

    # Step 2: Validate
    try:
        validate_yaml(yaml_data)
        print("YAML validated successfully.")
    except Exception as e:
        print(f" Validation failed: {e}")
        return

    # Step 3: Cache lookup
    config_manager = ConfigManager()
    config = config_manager.get_config(yaml_data)

    # Step 4: Save to output YAML
    with open(OUTPUT_YAML, "w") as f:
        yaml.dump(config, f, sort_keys=False)

    print(f"YAML written to {OUTPUT_YAML}")


    simulator_engine(config)


if __name__ == "__main__":
    main()
