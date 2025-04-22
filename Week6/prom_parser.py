import re
from collections import defaultdict

class PrometheusParser:
    def __init__(self, file_path):
        self.file_path = file_path
        self.pattern = re.compile(r'(\w+)\{([^}]*)\}\s+([\d.]+)\s+([\d.]+)')

    def parse(self):
        with open(self.file_path, "r") as f:
            lines = f.readlines()

        output_data = {
            "FileType": "prom",
            "Topic": "PDU Metrics"
        }
        metric_store = {}

        for line in lines:
            match = self.pattern.match(line)
            if not match:
                continue

            metric, labels_str, value_str, timestamp_str = match.groups()
            value = float(value_str)

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
            min_val = min(data["values"])
            max_val = max(data["values"])
            formatted_labels = list(data["labels"].keys())
            output_data[metric] = {
                "labels": formatted_labels,
                "value": [f"value({min_val}, {max_val})"],
                "timestamp": data["timestamp"]
            }

        return output_data
