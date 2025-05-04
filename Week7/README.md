# HPE Career Preview Program – Week 7

This repository contains a modular CLI tool and supporting code for simulating and producing telemetry data over Kafka. It supports Prometheus and JSON formats, converts them into a simulator-ready YAML format, and streams synthetic data to Kafka topics using a multithreaded producer.

## 📁 Repository Structure

```
Week7/
├── cli.py                  # Main CLI entry using `fire`
├── config_manager.py       # Converts Prometheus/JSON to simulator-ready YAML
├── prom_parser.py          # Prometheus Convertor
├── json_parser.py          # JSON Convertor
├── simulator.py            # Simulates metric data from YAML config
├── Producer.py             # Kafka producer supporting multiple topics & threads
├── Demo_Data/              # Sample input files (Prometheus & JSON)
│   ├── Current.json
│   ├── Voltage.json
│   ├── metrics_pdu.prom
│   ├── slurm_nodes.prom
│   └── slum_summary.prom
├── YAML/                   # Output directory for generated YAML config files
├── requirements.txt        # Python dependencies
```

---

## 🚀 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/prince-jain0/hpe-cpp.git
cd hpe-cpp/Week7
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Start Kafka Server

Ensure you have a Kafka broker running at `admin:9092` (or update the config in the CLI).

---

## 🚀 CLI Usage

You can launch the CLI in two ways:

### 🔹 Option 1: Interactive Menu (Recommended)

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
5. Exit
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

* **Option 5:** Exit the CLI.


---

## ❗ Error Handling

- Handles invalid YAML, missing files, permission errors, junk data, malformed metrics.
- Cache mechanism avoids regenerating YAML if config is unchanged.

---

## 📚 Dependencies

Key packages used:

- `fire` for CLI creation
- `yaml`, `json`, `pickle`, `ast` for data parsing and config management
- `confluent_kafka` for Kafka producer
- `threading`, `queue`, `time`, `random`, `datetime` for simulator logic

---
