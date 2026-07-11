# 53 — System Monitoring

> **Document 53 of 61** in the HeliosAI documentation set (see `README.md` → Repository Structure). Defines how we know the system is healthy.

---

## Table of Contents

1. [Purpose of This Document](#purpose-of-this-document)
2. [The Observability Stack](#the-observability-stack)
3. [Key Metrics Tracked](#key-metrics-tracked)
4. [Alerting](#alerting)

---

## Purpose of This Document

Data Drift (`49_Data_Drift.md`) monitors the *scientific* health of the models. This document covers the *software* health of the infrastructure.

## The Observability Stack

- **Metrics:** Prometheus scrapes metrics from the FastAPI apps and Kubernetes nodes.
- **Dashboards:** Grafana visualizes the Prometheus data (distinct from the scientific Dash application defined in `39_Dashboard.md`).
- **Logs:** Fluentbit forwards container stdout/stderr to an Elasticsearch/OpenSearch cluster.

## Key Metrics Tracked

- **Ingestion Lag:** The time difference between the timestamp of the latest record in the DB and `now()`. If this exceeds 5 seconds, the ingestion pipeline is failing.
- **Queue Depth:** The number of pending tasks in Celery/Redis.
- **API Latency:** The 95th percentile response time for the `/forecast` endpoint.
- **Model Inference Time:** Time taken for PyTorch/XGBoost to execute a `predict()` call.

## Alerting

If Ingestion Lag exceeds 30 seconds, or the API returns >5% 5xx errors, Prometheus Alertmanager fires a webhook to PagerDuty/Slack to wake up an on-call engineer.

**Next document:** `54_Secrets_Management.md`
