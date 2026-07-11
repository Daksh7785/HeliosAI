# 34 — Background Jobs

> **Document 34 of 61** in the HeliosAI documentation set (see `README.md` → Repository Structure). Defines the asynchronous task execution framework.

---

## Table of Contents

1. [Purpose of This Document](#purpose-of-this-document)
2. [Task Orchestration (Airflow vs. Celery)](#task-orchestration-airflow-vs-celery)
3. [Scheduled Jobs](#scheduled-jobs)
4. [Event-Driven Tasks](#event-driven-tasks)

---

## Purpose of This Document

HeliosAI runs numerous background processes that cannot block the main API thread. This document defines how these jobs are scheduled, queued, and executed.

## Task Orchestration (Airflow vs. Celery)

HeliosAI uses a two-tier background job system to handle both cron-like scheduling and real-time event-driven processing:

1. **Apache Airflow:** Used for complex, DAG-based scheduling. Examples include daily database backfills, weekly model retraining, and scheduled ingestion sweeps. Code lives in `airflow/dags/`.
2. **Celery:** Used for lightweight, fast-response tasks triggered by events (e.g., API requests). Code lives within the respective `services/*/worker.py` entrypoints.

## Scheduled Jobs

Defined in Airflow:
- `ingest_solexs_dag` / `ingest_hel1os_dag`: Periodically checks PRADAN for new data drops if streaming is unavailable.
- `model_retraining_dag`: Weekly process that pulls the latest Master Catalogue and fine-tunes the baseline forecasting models (`26_Machine_Learning.md`).
- `lead_time_reconciliation_dag`: Daily batch job computing the empirical lead-time metrics between forecasted triggers and actual peaks.

## Event-Driven Tasks

Defined in Celery (using Redis as the message broker):
- **On-Demand Ingestion:** Triggered by the CLI (`24_CLI.md`).
- **Explanation Generation:** Generating SHAP/Captum artifacts (`29_Explainable_AI.md`) is computationally heavy and is offloaded to a Celery worker immediately after a forecast is produced.

**Next document:** `35_Authentication.md`
