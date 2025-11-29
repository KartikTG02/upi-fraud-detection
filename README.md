# 🛡️ Real-Time UPI Transaction Fraud Detection System

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Kafka](https://img.shields.io/badge/Apache%20Kafka-Streaming-black)
![Redis](https://img.shields.io/badge/Redis-Caching-red)
![Postgres](https://img.shields.io/badge/PostgreSQL-Storage-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-ff4b4b)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED)

## 📌 Project Overview
This project is an end-to-end pipeline designed to detect fraudulent UPI transactions. It processes transaction streams, identifies suspicious patterns (High-Value or High-Velocity), and visualizes the data on a live dashboard.

It simulates a real-world FinTech environment where speed and data integrity are critical.

## 🏗️ System Architecture
The system follows a microservices-style architecture, fully containerized using Docker.

```mermaid
graph LR
    A[Transaction Generator] -->|JSON Stream| B(Apache Kafka)
    B -->|Subscribe| C[Fraud Engine / Consumer]
    C -->|Check Velocity| D[(Redis Cache)]
    D --Response--> C
    C -->|Flag & Store| E[(PostgreSQL DB)]
    E -->|Poll Data| F[Streamlit Dashboard]

