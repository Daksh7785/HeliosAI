# 26 — Machine Learning

> **Document 26 of 61.** Details the classical ML baseline layer of the Forecasting Engine (`23_Forecasting.md`), the first model generation in the progression described there. Precedes `27_Deep_Learning.md`.

---

## Table of Contents
1. [Purpose](#purpose)
2. [Model Choices](#model-choices)
3. [Feature Input](#feature-input)
4. [Class Imbalance Handling](#class-imbalance-handling)
5. [Hyperparameter Strategy](#hyperparameter-strategy)
6. [Evaluation Protocol](#evaluation-protocol)
7. [Revision History](#revision-history)

---

## Purpose

Specifies the gradient-boosted-tree baseline that ships first in Phase 4 (per `08_Development_Roadmap.md`), establishing the benchmark every subsequent deep-learning generation must beat before being adopted.

---

## Model Choices

- **XGBoost, LightGBM, CatBoost** — evaluated in parallel on identical folds; the best performer per flare class (not necessarily the same algorithm for every class) becomes the baseline reference.
- Chosen for: fast iteration, native handling of tabular engineered features (no sequence modeling needed for this generation), and built-in feature importance supporting `29_Explainable_AI.md`'s SHAP integration.

---

## Feature Input

Consumes the full per-band, cross-band, and temporal/precursor feature table from `21_Feature_Engineering.md`, flattened into a single feature vector per prediction time point (in contrast to deep sequence models in `27`/`28`, which consume the raw windowed sequence).

---

## Class Imbalance Handling

Given the rarity of high-class flares (Risk R2, `10_Risk_Assessment.md`): class weighting, focal-loss-style objective adaptation where supported, and SMOTE-style oversampling on the tabular feature space (per `README.md` → Evaluation Criteria Alignment). Oversampling is applied only to training folds, never to validation/test folds, to avoid inflating reported performance.

---

## Hyperparameter Strategy

Bayesian or grid search per flare class, tracked in MLflow (per `24_AI_Architecture.md`'s shared registry), with the search space and final chosen parameters both logged for reproducibility.

---

## Evaluation Protocol

- Time-based (not random) train/validation/test splits, to avoid leaking future information into training — critical for a forecasting task.
- Metrics: per-class precision/recall (TPR/FAR per `README.md` → Evaluation Criteria Alignment), calibration curves, and empirical lead time (per `23_Forecasting.md`) computed identically to how deep models will later be evaluated, ensuring apples-to-apples comparison in Phase 4.

**Next document:** `27_Deep_Learning.md` — say **NEXT** to continue.

---

## Revision History
| Version | Date | Author | Notes |
|---|---|---|---|
| 0.1 | 2026-07-12 | HeliosAI Documentation | Initial Machine Learning baseline spec — model choice, imbalance handling, evaluation protocol |
