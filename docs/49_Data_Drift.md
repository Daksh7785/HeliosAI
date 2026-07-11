# 49 — Data Drift Monitoring

> **Document 49 of 61** in the HeliosAI documentation set (see `README.md` → Repository Structure). Defines how the system detects when input data changes fundamentally.

---

## Table of Contents

1. [Purpose of This Document](#purpose-of-this-document)
2. [Types of Drift](#types-of-drift)
3. [Detection Mechanisms](#detection-mechanisms)
4. [Handling Drift](#handling-drift)

---

## Purpose of This Document

This document outlines the final piece of the MLOps puzzle: monitoring the live data stream to ensure it still resembles the data the model was trained on.

## Types of Drift

1. **Concept Drift:** The underlying physics or definition of a "flare" changes (rare).
2. **Data Drift (Covariate Shift):** The distribution of the input features changes. For example, as the solar cycle peaks, the baseline background flux rises significantly. A model trained during solar minimum will interpret this new baseline as a constant anomaly.

## Detection Mechanisms

HeliosAI uses statistical tests (e.g., Kolmogorov-Smirnov test, Population Stability Index) to compare the feature distributions of the live incoming data (last 7 days) against the feature distributions of the holdout test set used during the active model's training run.
This is implemented as an Airflow DAG (`data_drift_dag`) running daily using the `Evidently` Python library.

## Handling Drift

If the drift score crosses a predefined threshold, the system:
1. Logs a high-priority warning to the Dashboard (`39_Dashboard.md`).
2. Triggers the Continuous Training DAG (`47_Continuous_Training.md`) to automatically attempt to fit a new model to the recent data.

**Next document:** `50_Infrastructure.md`
