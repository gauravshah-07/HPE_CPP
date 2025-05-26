# import re
# from collections import defaultdict
# import os

# class PrometheusParser:
#     def __init__(self, file_path, topic):
#         self.file_path = file_path
#         self.topic = topic
#         self.pattern = re.compile(r'(\w+)\{([^}]*)\}\s+([\d.]+)\s+([\d.]+)')
#         self.label_value_overrides = {}  # key -> set of values from user files

#     def _parse_labels(self, labels_str):
#         label_pattern = re.compile(r'(\w+)="(.*?)"')
#         return {k: v for k, v in label_pattern.findall(labels_str)}

#     def _group_by_prefix(self, values):
#         grouped = defaultdict(set)
#         for val in values:
#             match = re.match(r'^[a-zA-Z\-]+', val)
#             prefix = match.group(0) if match else val[:4]
#             grouped[prefix].add(val)
#         return grouped

#     def _load_label_values_from_file(self, label_key, file_path):
#         try:
#             with open(file_path, 'r') as f:
#                 values = {line.strip() for line in f if line.strip()}
#                 print(f"[INFO] Loaded {len(values)} values for label '{label_key}' from file '{file_path}'.")
#                 return values
#         except Exception as e:
#             print(f"[ERROR] Could not load file for '{label_key}': {e}")
#             return set()

#     def _prompt_label_sources(self, all_labels):
#         print("\n--- Label Value Source Setup ---")
#         for label in sorted(all_labels):
#             choice = input(f"Do you want to provide a file for label '{label}'? (y/n): ").strip().lower()
#             if choice == 'y':
#                 file_path = input(f"Enter file path for label '{label}': ").strip()
#                 self.label_value_overrides[label] = self._load_label_values_from_file(label, file_path)
#             else:
#                 print(f"[INFO] Will extract values for '{label}' from the Prometheus file.")

#     def parse(self):
#         with open(self.file_path, "r") as f:
#             lines = f.readlines()

#         output_data = {
#             "filetype": "prom",
#             "topic": self.topic
#         }

#         metric_store = {}
#         all_label_keys = set()

#         # First pass: parse labels and values
#         for line in lines:
#             line = line.strip()
#             if not line or line.startswith("#"):
#                 continue

#             match = self.pattern.match(line)
#             if not match:
#                 continue

#             metric, labels_str, value_str, timestamp_str = match.groups()
#             value = float(value_str)
#             labels_dict = self._parse_labels(labels_str)
#             all_label_keys.update(labels_dict.keys())

#             if metric not in metric_store:
#                 metric_store[metric] = {
#                     "labels": defaultdict(set),
#                     "values": [],
#                     "timestamp": "<current_timestamp>"
#                 }

#             for k, v in labels_dict.items():
#                 metric_store[metric]["labels"][k].add(v.strip())

#             metric_store[metric]["values"].append(value)

#         # Prompt for each label's source (user-provided file or extract from Prometheus)
#         self._prompt_label_sources(all_label_keys)

#         # Final output formatting
#         for metric, data in metric_store.items():
#             min_val = min(data["values"])
#             max_val = max(data["values"])

#             formatted_labels = {}
#             for label_key, values in data["labels"].items():
#                 # Use user-provided values if available
#                 values_to_group = self.label_value_overrides.get(label_key, values)
#                 grouped = self._group_by_prefix(values_to_group)
#                 formatted_labels[label_key] = [
#                     "{" + ", ".join(sorted(group)) + "}" for group in grouped.values()
#                 ]

#             output_data[metric] = {
#                 "labels": [formatted_labels],
#                 "value": [f"({min_val}, {max_val})"],
#                 "timestamp": data["timestamp"]
#             }

#         return output_data

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

    def _group_by_prefix(self, values):
        """
        Groups label values by common prefix (letters/hyphens before digits).
        E.g., 'antero-turin-500w01' and 'antero-turin-500w02' get grouped together.
        """
        grouped = defaultdict(set)
        for val in values:
            match = re.match(r'^[a-zA-Z\-]+', val)
            prefix = match.group(0) if match else val[:4]
            grouped[prefix].add(val)
        return grouped

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

            formatted_labels = {}
            for k, values in data["labels"].items():
                grouped = self._group_by_prefix(values)
                formatted_labels[k] = [
                    "" + ", ".join(sorted(group)) + "" for group in grouped.values()
                ]

            output_data[metric] = {
                "labels": [formatted_labels],
                "value": [f"({min_val}, {max_val})"],
                "timestamp": data["timestamp"]
            }

        return output_data
