# Distributed Real-Time UPI Fraud Detection System

![Spark](https://img.shields.io/badge/Apache%20Spark-Distributed-orange)
![Kafka](https://img.shields.io/badge/Apache%20Kafka-Streaming-black)
![Redis](https://img.shields.io/badge/Redis-Caching-red)
![Postgres](https://img.shields.io/badge/PostgreSQL-Storage-blue)
![Docker](https://img.shields.io/badge/Docker-Microservices-2496ED)
![Parquet](https://img.shields.io/badge/Parquet-Data%20Lake-green)

## Project Overview
This project is an **Event-Driven Big Data Pipeline** designed to detect financial fraud in high-throughput UPI transaction streams. 

Unlike traditional rule-based systems, this engine uses **Apache Spark Structured Streaming** to perform stateful, windowed aggregations in real-time. It calculates **Z-Scores** (Standard Deviation) to detect statistical anomalies and persists data into a **Partitioned Data Lake** for historical analysis.

##  System Architecture

```mermaid
graph LR
    A[Kafka Stream] --> B(Apache Spark)
    
    subgraph "Spark Processing"
    B -->|Calculate Z-Scores| B
    end
    
    B -->|Path 1: Cold Storage| C[Parquet Data Lake]
    B -->|Path 2: Hot Storage| D[(Postgres DB)]
    D -->|Visualize| E[Streamlit Dashboard]

```
## Dashboard Preview
<img width="1087" height="748" alt="image" src="https://github.com/user-attachments/assets/86101c61-53b2-4f36-b3c6-7ba5b229aa59" />

