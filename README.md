# HPE Career Preview Program Project
## Overview
This repository is for code sharing and progress updates related to the HPE Career Preview Program Project.

# Progress
## Week 1
- **Completed:**
  1. Learned the basics of Apache Kafka
  2. Set up Kafka on a Virtual Machine (VM)
  3. Set up Kafka on Docker

## Week 2
- **Completed:**
  1. Created a Kafka producer-consumer with syslog JSON data on the terminal
  2. Implemented the same Kafka producer-consumer using Python
## Week 3
- **Completed:**
  1. Connected Kafka producer and consumer on different machines using ngrok
  2. Generated synthetic system logs using Python and sent them over Kafka
  3. Installed Telegraf
     
## Week 4
- **Completed:**
  1. Created Python scripts to generate random telemetry data
  2. Implemented multiple Kafka producers for different telemetry types
  3. Designed a producer menu system for managing Kafka producers interactively
  4. Containerized the producer scripts using Docker

## Week 5
- **Completed:**
  1. Reading metrics data from Prometheus formatted files and telemetry JSON files, extracting metric names, labels, values, and timestamps.
  2. Extracted data is converted into a simulator-ready YAML format, where values are represented as ranges and labels are grouped by unique values.
  3. Configuration Manager implements caching mechanism to avoid regenerating YAML files for already-processed configurations, using hash-based identification.
  
## Week 6
- **Completed:**
  1. Built the simulator engine to manage multiple metric simulators concurrently using threads, allowing parallel data generation and Kafka publishing.
  2. Developed a multi-threaded Kafka producer to read from configurable YAML files and continuously publish synthetic metrics to respective topics.
  3. Implemented a Kafka consumer receives both structured JSON and Prometheus-style messages from topics like PDU and Telemetry.

## Week 7

- **Completed:**

  1. Fixed and improved Prometheus and JSON data converters by handling edge cases, ensuring accurate label and value extraction, and improving YAML output formatting.
  2. Designed and implemented a unified Command-Line Interface (CLI) for the entire simulation pipeline using Python Fire, including support for:
     * Converting JSON/Prometheus files to YAML topic configurations.
     * Generating one-sample synthetic data from a topic.
     * Running Kafka producers interactively with topic-based configuration.
     * Configuring broker connection dynamically.
  3. Integrated a user-friendly interactive menu system to guide users through CLI operations, supporting both beginners and advanced users.
 

  
## Week 8

- **Completed:**

  1. CLI was improved to display the list of topics
  2. CLI file was made to use Argparse instead of Fire
  3. Caching of topics was integrated
  4. Added the feature of saving the user configuration
  5. Feature of creating topic in kafka based on input was added.



 ## Week 9

- **Completed:**

  1. Label values extraction is made optional. User can give custom label values.
  2. Range of values for each topic can be taken from user input (optional).
  3. Custom nodelist can be taken as input from the user in text file format.
  4. CLI was modified.   
