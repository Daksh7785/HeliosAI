# 48 — Feature Store

> **Document 48 of 61** in the HeliosAI documentation set (see `README.md` → Repository Structure). Defines the management of engineered features.

---

## Table of Contents

1. [Purpose of This Document](#purpose-of-this-document)
2. [Why a Feature Store?](#why-a-feature-store)
3. [Offline vs. Online Store](#offline-vs-online-store)
4. [Implementation Details](#implementation-details)

---

## Purpose of This Document

The Feature Engineering layer (`21_Feature_Engineering.md`) calculates values like rolling variance and spectral hardness. The Feature Store is where these values are persisted to ensure consistency between training (offline) and inference (online).

## Why a Feature Store?

Training-serving skew is a massive problem in MLOps. If a data scientist uses a 5-minute rolling average script in Jupyter for training, but the backend engineer implements a 3-minute rolling average in FastAPI for serving, the model will output garbage. A Feature Store ensures the exact same definition is used in both places.

## Offline vs. Online Store

- **Offline Store:** TimescaleDB historical tables. Used for batch extraction to train models via the Continuous Training DAG (`47_Continuous_Training.md`). Prioritizes high throughput for large datasets.
- **Online Store:** Redis. Used by the FastAPI Serving layer. Prioritizes ultra-low latency (<5ms) retrieval of the *latest* feature vectors for real-time inference.

## Implementation Details

HeliosAI uses `Feast` as the feature store abstraction layer. `Feast` manages the definitions (in a Git repository) and handles the materialization of features from TimescaleDB (offline) into Redis (online).

**Next document:** `49_Data_Drift.md`
