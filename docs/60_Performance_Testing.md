# 60 — Performance Testing

> **Document 60 of 61** in the HeliosAI documentation set (see `README.md` → Repository Structure). Defines stress and load testing.

---

## Table of Contents

1. [Purpose of This Document](#purpose-of-this-document)
2. [Load Testing with Locust](#load-testing-with-locust)
3. [Stress Scenarios](#stress-scenarios)
4. [Latency Budgets](#latency-budgets)

---

## Purpose of This Document

HeliosAI must perform under pressure. If a massive solar event occurs, traffic to the Dashboard will spike precisely when the ingestion and processing subsystems are working hardest.

## Load Testing with Locust

HeliosAI uses `Locust` (a Python-based load testing tool) to simulate thousands of concurrent users hitting the API and opening WebSocket connections.

## Stress Scenarios

1. **The Carrington Simulation:** Flooding the ingestion API with simulated payloads at 10x the normal cadence to ensure the TimescaleDB hypertable ingest rate does not bottleneck.
2. **The Reddit Hug of Death:** Simulating 5,000 concurrent WebSocket clients subscribing to the `channel:telemetry:fused` topic to verify Redis Pub/Sub and FastAPI connection handling.

## Latency Budgets

Performance tests assert against strict budgets:
- **Ingestion to Prediction:** < 2 seconds. (Time from raw payload arriving to a forecast being broadcast).
- **API P99 Latency:** < 200ms for standard REST endpoints under heavy load.

**Next document:** `61_Glossary.md`
