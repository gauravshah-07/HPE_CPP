import re
from collections import defaultdict

class PrometheusParser:
    def __init__(self, file_path, topic):
        self.topic = topic
        self.file_path = file_path
        self.pattern = re.compile(r'(\w+)\{([^}]*)\}\s+([\d.]+)\s+([\d.]+)')

    def _parse_labels(self, labels_str):
        label_pattern = re.compile(r'(\w+)="(.*?)"')
        return {k: v for k, v in label_pattern.findall(labels_str)}

    def parse(self):
        with open(self.file_path, "r") as f:
            lines = f.readlines()

        output_data = {
            "filetype": "prom",
            "topic": self.topic
        }

        metric_store = {}

        for line in lines:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            match = self.pattern.match(line)
            if not match:
                continue

            metric, labels_str, value_str, timestamp_str = match.groups()
            value = float(value_str)

            labels_dict = self._parse_labels(labels_str)

            if metric not in metric_store:
                metric_store[metric] = {
                    "labels": defaultdict(set),
                    "values": [],
                    "timestamp": "<current_timestamp>"
                }

            for k, v in labels_dict.items():
                for val in v.split(','):
                    metric_store[metric]["labels"][k].add(val.strip())
            metric_store[metric]["values"].append(value)

        for metric, data in metric_store.items():
            min_val = min(data["values"])
            max_val = max(data["values"])
            formatted_labels = [{k: sorted(list(v))} for k, v in data["labels"].items()]
            output_data[metric] = {
                "labels": formatted_labels,
                "value": [f"({min_val}, {max_val})"],
                "timestamp": data["timestamp"]
            }

        return output_data
    
"""
def main():
    file_path = "Samples/slurm_summary.log.txt"
    topic = "PDU Metrics"
    output_path = "parsed_output.yaml"

    parser = PrometheusParser(file_path, topic)
    parsed_data = parser.parse()

    with open(output_path, "w") as f:
        yaml.dump(parsed_data, f, sort_keys=False)

    print(f"YAML for simulator generated in '{output_path}'")

if __name__ == "__main__":
    main()
"""