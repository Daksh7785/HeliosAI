# 46 — Experiment Tracking

> **Document 46 of 61** in the HeliosAI documentation set (see `README.md` → Repository Structure). Defines how model training runs are logged.

---

## Table of Contents

1. [Purpose of This Document](#purpose-of-this-document)
2. [What Gets Logged?](#what-gets-logged)
3. [Tracking Structure](#tracking-structure)
4. [Integration with Airflow](#integration-with-airflow)

---

## Purpose of This Document

Experiment Tracking provides reproducibility. If a model in production behaves poorly, data scientists must be able to trace exactly what code, data, and parameters produced it.

## What Gets Logged?

For every training run, the MLflow Tracking Server logs:
- **Parameters:** Learning rate, batch size, tree depth, etc.
- **Metrics:** True Skill Statistic (TSS), Heidke Skill Score (HSS), F1-Score, and Loss over epochs.
- **Tags:** Git commit hash of the training code, Airflow Run ID, and the data cutoff timestamp.
- **Artifacts:** Feature importance plots, SHAP summary charts, and the model binary itself.

## Tracking Structure

Experiments are grouped logically:
- `Experiment: baseline-xgboost`
- `Experiment: sequence-lstm`
- `Experiment: transformer-tft`

## Integration with Airflow

The scheduled training DAGs (`34_Background_Jobs.md`) wrap their execution in `mlflow.start_run()`. If a run achieves a higher TSS than the current `Production` model, the Airflow DAG automatically registers it to the Model Registry (`45_Model_Registry.md`) and transitions it to `Staging`.

**Next document:** `47_Continuous_Training.md`
