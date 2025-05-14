import json
import yaml
from collections import defaultdict, OrderedDict

def represent_ordereddict(dumper, data):
    return dumper.represent_dict(data.items())
yaml.add_representer(OrderedDict, represent_ordereddict)

def convert_to_yaml(data, metric_name, topic):
    grouped_data = defaultdict(lambda: defaultdict(list))
    value_key = "Value"
    label_keys = set()

    for entry in data:
        for key in entry:
            if key != value_key and not isinstance(entry[key], dict):
                label_keys.add(key)
            elif isinstance(entry[key], dict) and "string" in entry[key]:
                label_keys.add(key)

    for entry in data:
        labels = {}
        for key in label_keys:
            if key == "Timestamp":
                labels[key] = "<current_timestamp>"
            elif isinstance(entry[key], dict) and "string" in entry[key]:
                labels[key] = entry[key]["string"]
            else:
                labels[key] = entry[key]
        grouped_data[metric_name]["labels"].append(labels)
        grouped_data[metric_name]["value"].append(entry[value_key])

    result = OrderedDict()
    result["filetype"] = 'json'
    result["topic"] = topic
    result[metric_name] = OrderedDict()
    result[metric_name]["labels"] = []

    label_sets = defaultdict(set)
    for label_group in grouped_data[metric_name]["labels"]:
        for label, value in label_group.items():
            if value is not None:
                label_sets[label].add(value)
    for label, value_set in label_sets.items():
        result[metric_name]["labels"].append({label: sorted(list(value_set))})

    min_value = min(grouped_data[metric_name]["value"])
    max_value = max(grouped_data[metric_name]["value"])
    result[metric_name]["value"] = [f"({min_value}, {max_value})"]
    result[metric_name]["timestamp"] = "<current_timestamp>"

    return result  


def convert_file(input_file, output_file, metric_name, topic):
    with open(input_file, 'r') as infile:
        data = json.load(infile)
    if not metric_name:
        if isinstance(data, list) and "MessageId" in data[0]:
            metric_name = data[0]["MessageId"]
        else:
            raise ValueError("Cannot infer metric name: MessageId missing in input.")

    yaml_output = convert_to_yaml(data, metric_name, topic)
    print(yaml_output)
    return yaml_output
