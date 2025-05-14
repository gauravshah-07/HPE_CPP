# HPE Career Preview Program – Week 8

This repository contains a modular CLI tool and supporting code for simulating and producing telemetry data over Kafka. It supports Prometheus and JSON formats, converts them into a simulator-ready YAML format, and streams synthetic data to Kafka topics using a multithreaded producer.

##  Repository Structure

```
Week8/
├── CLI.py                        # Main CLI for User Interaction
├── yaml-schema.txt               # YAML schema definition 
├── config_manager/
│   ├── config_manager.py         # Core logic for managing config conversions
│   ├── json_parser.py            # JSON → YAML parser
│   └── prom_parser.py            # Prometheus → YAML parser
├── consumer/
│   └── consumer.py               # Kafka consumer (for testing)
├── producer/
│   └── Producer.py               # Kafka producer (multithreaded, multi-topic)
├── simulator/
│   └── simulator.py              # Metric simulator using YAML config
|── Sample_Data/                  # Sample Test Files
```

---

##  Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/prince-jain0/hpe-cpp.git
cd hpe-cpp/Week8
```

### 2. Start Kafka Server

Ensure you have a Kafka broker running at `admin:9092` (or update the config in the CLI).

---

##  CLI Usage


### Interactive Menu 

Run:

```bash
python cli.py
```

You'll see a user-friendly interactive menu like this:

```
CLI MENU
------------------------
1. Create YAML from Prometheus
2. Create YAML from JSON
3. Generate one sample data from topic
4. Kafka Producer Menu
5. List all available topics
6. Exit
```

Each option lets you perform actions step-by-step:

* **Option 1:** Converts a Prometheus `.prom` file into a YAML configuration.

* **Option 2:** Converts a JSON file into a YAML configuration. You can optionally specify the metric name.

* **Option 3:** Generates and displays one sample simulated metric from a given topic's YAML config.

* **Option 4:** Opens the Kafka producer submenu:

  ```
  PRODUCER MENU
  ------------------------
  1. Configure Kafka broker
  2. Run producer for topics
  3. Back to main menu
  ```

  * `Configure Kafka broker`: Set your Kafka bootstrap server (default is `admin:9092`)
  * `Run producer for topics`: Input topic names (comma-separated) to start producing simulated metrics.

* **Option 5:** Lists the topics present in simulator.

* **Option 6:** Exit the CLI.
---

##  Error Handling

- Handles invalid YAML, missing files, permission errors, junk data, malformed metrics.
- Cache mechanism avoids regenerating YAML if config is unchanged.

---

##  Dependencies

Key packages used:

- `yaml`, `json`, `pickle`, `ast` for data parsing and config management
- `confluent_kafka` for Kafka producer
- `threading`, `queue`, `time`, `random`, `datetime` for simulator logic
---
