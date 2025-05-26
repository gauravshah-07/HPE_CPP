
import yaml
import random
import time
from datetime import datetime, timezone
import ast
from config_manager.config_manager import ConfigManager

class MetricSimulator:
    def __init__(self, config_path):
        self.config_path = config_path
        self.config_manager = ConfigManager()
        self.config = self.load_config()
        self.filetype = self.config.get('filetype', '').lower()
        self.topic = self.config.get('topic')
        self.label_overrides = self.prompt_label_file_input()

    def load_config(self):
        cached_config = self.config_manager.get_config(self.config_path)
        if cached_config:
            print(f"Loaded config from cache: {self.config_path}")
            return cached_config
        else:
            with open(self.config_path, 'r') as f:
                config = yaml.safe_load(f)
            self.config_manager.cache_config(self.config_path, config)
            print(f"Cached config: {self.config_path}")
            return config

    def prompt_label_file_input(self):
        label_file_data = {}
        choice = input("Do you want to input a label values text file? (y/n): ").strip().lower()
        if choice == 'y':
            try:
                file_path = input("Enter the path to the label file (YAML or plain text): ").strip()
                if file_path.endswith('.yaml') or file_path.endswith('.yml'):
                    with open(file_path, 'r') as f:
                        label_file_data = yaml.safe_load(f)
                        print(f"[INFO] Loaded label overrides from YAML: {file_path}")
                else:
                    with open(file_path, 'r') as f:
                        lines = [line.strip() for line in f if line.strip()]
                        # Put all into a generic label key
                        label_file_data = {"custom_label": lines}
                        print(f"[INFO] Loaded {len(lines)} values from text file.")
            except Exception as e:
                print(f"[ERROR] Failed to load label file: {e}")
        else:
            print("[INFO] No label override file provided.")
        return label_file_data

    def getTopic(self):
        return self.topic

    def simulate_metrics(self,value_ranges=None):
        msgs = []
        for metric_name, metric_def in self.config.items():
            if metric_name in ['filetype', 'topic']:
                continue
            labels = self.flatten_labels(metric_def.get('labels', []))
            if value_ranges and len(value_ranges) > 0:
                ranges = (list(value_ranges[0]))
            else:
                ranges = metric_def.get('value', [])
            timestamp = int(datetime.now(timezone.utc).timestamp() * 1000)
            value = self.generate_value(ranges)

            metric_data = self.format_metric(metric_name, labels, value, timestamp)
            msgs.append((metric_data, self.filetype))
            print(metric_data)
        return msgs

    def generate_value(self, ranges):
        if not ranges:
            return 0.0
        if isinstance(ranges, str):
            try:
                ranges = ast.literal_eval(ranges)
            except Exception:
                return 0.0
        if isinstance(ranges, list) and len(ranges) == 1 and isinstance(ranges[0], str):
            try:
                ranges = ast.literal_eval(ranges[0])
            except Exception:
                return 0.0
        if isinstance(ranges, (list, tuple)) and len(ranges) >= 2:
            low, high = float(ranges[0]), float(ranges[1])
            return round(random.uniform(low, high), 0)
        return 0.0

    def flatten_labels(self, label_list):
        flat = {}
        for label in label_list:
            for k, v in label.items():
                if k in self.label_overrides:
                    flat[k] = random.choice(self.label_overrides[k])
                else:
                    flat[k] = random.choice(v)
        return flat

    def format_metric(self, name, labels, value, timestamp):
        if self.filetype == 'prom':
            label_str = ','.join([f'{k}="{v}"' for k, v in labels.items()])
            return f'{name}{{{label_str}}} {value} {int(timestamp)}'

        elif self.filetype == 'json':
            formatted = {
                "MessageId": name,
                "Timestamp": int(timestamp),
                "Value": value
            }

            for k, v in labels.items():
                if v is None:
                    formatted[k] = None
                elif isinstance(v, int):
                    formatted[k] = {"int": v}
                elif isinstance(v, float):
                    formatted[k] = v
                elif isinstance(v, str):
                    if v.isdigit():
                        formatted[k] = {"int": int(v)}
                    else:
                        try:
                            float_val = float(v)
                            formatted[k] = {"float": float_val}
                        except ValueError:
                            formatted[k] = {"string": v}
                else:
                    formatted[k] = {"string": str(v)}

            return formatted

        else:
            raise ValueError("Unsupported filetype: must be 'prom' or 'json'")


if __name__ == '__main__':
    import sys
    simulator = MetricSimulator(sys.argv[1])
    while True:
        simulator.simulate_metrics()
        time.sleep(2)
