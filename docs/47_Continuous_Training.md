# 47 — Continuous Training (CT)

> **Document 47 of 61** in the HeliosAI documentation set (see `README.md` → Repository Structure). Defines the automated retraining pipeline.

---

## Table of Contents

1. [Purpose of This Document](#purpose-of-this-document)
2. [Triggers for Retraining](#triggers-for-retraining)
3. [The Retraining DAG](#the-retraining-dag)
4. [Shadow Mode Evaluation](#shadow-mode-evaluation)

---

## Purpose of This Document

Models degrade over time as the solar cycle progresses. Continuous Training (CT) automates the process of incorporating new Master Catalogue events into the models.

## Triggers for Retraining

1. **Schedule-Based:** A cron trigger in Airflow initiates a retrain on the first of every month.
2. **Performance-Based:** If the Data Drift monitor (`49_Data_Drift.md`) detects a significant shift in feature distributions, it fires a webhook to trigger the DAG immediately.

## The Retraining DAG

The Airflow DAG executes the following sequence:
1. **Data Pull:** Extract all events from the Master Catalogue up to `now()`.
2. **Split:** Create Train/Validation/Test sets (chronological split, not random, to prevent data leakage in time-series).
3. **Train:** Fit the model and log to MLflow (`46_Experiment_Tracking.md`).
4. **Evaluate:** Calculate TSS and HSS on the test set.
5. **Promote:** If metrics > current production model, register to `Staging`.

## Shadow Mode Evaluation

Before promoting a `Staging` model to `Production`, HeliosAI can run it in "Shadow Mode". The API (`services/api/`) passes incoming live data to *both* the Production and Staging models, but only returns the Production forecast to the user. The Staging forecasts are logged to the database for parallel comparison.

**Next document:** `48_Feature_Store.md`
