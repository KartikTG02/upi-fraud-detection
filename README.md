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
    A[Traffic Generator] -->|JSON Stream| B(Apache Kafka)
    B -->|Ingest| C[Spark Master / Workers]
    
    subgraph "Distributed Processing Layer"
    C -->|Watermarking & Windows| C
    C -->|Check State| D[(Redis)]
    end
    
    C -->|Anomalies| E[(PostgreSQL)]
    C -->|All Data| F[Parquet Data Lake]
    E -->|Poll| G[Streamlit Dashboard]

