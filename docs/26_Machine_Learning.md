# 26 — Machine Learning (Baseline Models)

> **Document 26 of 61** in the HeliosAI documentation set (see `README.md` → Repository Structure). Details the baseline classical machine learning models used in the Forecasting Engine (`23_Forecasting.md`).

---

## Table of Contents

1. [Purpose of This Document](#purpose-of-this-document)
2. [Why Baseline Models?](#why-baseline-models)
3. [Model Architectures](#model-architectures)
4. [Feature Selection](#feature-selection)
5. [Training Pipeline](#training-pipeline)

---

## Purpose of This Document

This document specifies the classical machine learning models used for flare forecasting. These models establish the performance baseline against which deeper neural networks (`27_Deep_Learning.md`, `28_Transformer_Models.md`) are evaluated.

## Why Baseline Models?

Before deploying complex sequence models, HeliosAI relies on gradient-boosted trees. They provide:
- **Fast Training and Inference:** Ideal for rapid prototyping and deployment on constrained hardware.
- **Inherent Explainability:** Built-in feature importance scores align seamlessly with the Explainable AI requirements (`29_Explainable_AI.md`).
- **Robustness:** Tree-based models handle tabular feature sets and missing data exceptionally well.

## Model Architectures

The forecasting engine implements three primary baseline models:
1. **XGBoost:** The primary workhorse for classification tasks.
2. **LightGBM:** Used for faster training iterations and lower memory footprints.
3. **CatBoost:** Leveraged if categorical features (e.g., active region classifications, if integrated later) become significant.

## Feature Selection

These models consume aggregated statistical features derived from the rolling window (e.g., max, min, mean, variance, and gradient of flux and hardness ratio over the last 60 minutes) rather than raw time-series steps.

## Training Pipeline

The training pipeline integrates directly with MLflow (`44_MLOps.md`) to log hyperparameters, metrics, and serialized model artifacts. 

**Next document:** `27_Deep_Learning.md`
