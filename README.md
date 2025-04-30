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



