# 45 — Model Registry

> **Document 45 of 61** in the HeliosAI documentation set (see `README.md` → Repository Structure). Defines how trained models are versioned and stored.

---

## Table of Contents

1. [Purpose of This Document](#purpose-of-this-document)
2. [The MLflow Registry](#the-mlflow-registry)
3. [Model Stages](#model-stages)
4. [Loading Models in Production](#loading-models-in-production)

---

## Purpose of This Document

When the continuous training pipeline (`47_Continuous_Training.md`) finishes running, the resulting model needs a secure, versioned home before it can be used for live forecasting.

## The MLflow Registry

HeliosAI uses the MLflow Model Registry.
- **Backend Store:** The core PostgreSQL database (`30_Database_Design.md`) holds the MLflow metadata (versions, stages, tags).
- **Artifact Store:** An S3-compatible object store (e.g., MinIO or AWS S3) holds the actual binary weights (`.pkl` for XGBoost, `.pt` for PyTorch).

## Model Stages

Every model in the registry exists in one of four stages:
1. `None`: A newly trained model, awaiting evaluation.
2. `Staging`: A model currently being evaluated against a holdout test set or running in shadow mode.
3. `Production`: The active model currently serving the `/api/v1/forecast` endpoints.
4. `Archived`: A deprecated model kept for reproducibility and auditing.

## Loading Models in Production

When the `services/api/` pods boot, they query the MLflow REST API to find the URI of the model currently tagged as `Production`, download the weights from the Artifact Store into memory, and begin serving predictions.

**Next document:** `46_Experiment_Tracking.md`
