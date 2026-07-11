# 44 — MLOps Overview

> **Document 44 of 61** in the HeliosAI documentation set (see `README.md` → Repository Structure). Introduces the Machine Learning Operations lifecycle.

---

## Table of Contents

1. [Purpose of This Document](#purpose-of-this-document)
2. [Why MLOps for Space Weather?](#why-mlops-for-space-weather)
3. [The MLOps Lifecycle in HeliosAI](#the-mlops-lifecycle-in-heliosai)
4. [Tooling Choices](#tooling-choices)

---

## Purpose of This Document

HeliosAI is not a static academic script; it is a continuously evolving operational system. This document outlines the MLOps layer that ensures the Forecasting Engine (`23_Forecasting.md`) remains accurate over the 11-year solar cycle.

## Why MLOps for Space Weather?

The sun's behavior changes dramatically between solar minimum and solar maximum. A model trained on 2024 data (approaching maximum) might overpredict flares in 2028 (approaching minimum) if not retrained. MLOps automates the detection of this drift and handles retraining.

## The MLOps Lifecycle in HeliosAI

1. **Tracking:** Logging hyperparameters and evaluation metrics during training (`46_Experiment_Tracking.md`).
2. **Registry:** Versioning the resulting `.pkl` or `.pt` model artifacts (`45_Model_Registry.md`).
3. **Serving:** The API (`31_Backend_Architecture.md`) loading the active model.
4. **Monitoring:** Checking for statistical deviations in the incoming SoLEXS/HEL1OS flux (`49_Data_Drift.md`).
5. **Continuous Training:** Automated Airflow DAGs triggering retraining when drift occurs or new ground-truth labels are established (`47_Continuous_Training.md`).

## Tooling Choices

HeliosAI standardizes on **MLflow** for Experiment Tracking and Model Registry, integrating seamlessly with the existing Python stack and PostgreSQL database.

**Next document:** `45_Model_Registry.md`
