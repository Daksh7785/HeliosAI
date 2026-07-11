# 23 — Forecasting Engine

> **Document 23 of 61** in the HeliosAI documentation set (see `README.md` → Repository Structure). Defines Phase 4 of the system, consuming the fused feature vector from `21_Feature_Engineering.md` and the master catalogue from `22_Nowcasting.md`.

---

## Table of Contents

1. [Purpose of This Document](#purpose-of-this-document)
2. [What is Forecasting in HeliosAI?](#what-is-forecasting-in-heliosai)
3. [Precursor Feature Window](#precursor-feature-window)
4. [Forecasting Models Architecture](#forecasting-models-architecture)
5. [Lead-Time Reconciler](#lead-time-reconciler)
6. [Training and Evaluation Strategy](#training-and-evaluation-strategy)
7. [Output Contract](#output-contract)

---

## Purpose of This Document

This document outlines the design and implementation of the **Forecasting Engine**. While the nowcasting engine detects flares as they happen, the forecasting engine is responsible for predicting flares *before* they occur, leveraging the hard X-ray precursors detected by HEL1OS alongside the soft X-ray baseline from SoLEXS.

## What is Forecasting in HeliosAI?

Forecasting involves predicting the probability of a solar flare (parameterized by target class and horizon) using historical data windows. Specifically:
- **Horizon Options:** Short-term (e.g., +15m, +30m) to medium-term (+60m).
- **Output:** A calibrated probability score [0.0 - 1.0] for reaching a specific flare class threshold (e.g., M-class or X-class) within the specified horizon.

## Precursor Feature Window

The input to the forecasting models is a **rolling feature window** (e.g., T-60m to T) constructed from the engineered features derived in `21_Feature_Engineering.md`. Key features include:
- Temporal gradients of SoLEXS flux.
- Impulsive spike indicators from HEL1OS.
- **Spectral Hardness Ratio** (HEL1OS flux / SoLEXS flux) - the primary precursor metric.
- Wavelet-domain energy distributions.

## Forecasting Models Architecture

HeliosAI employs a progressive modeling approach, moving from interpretable baselines to complex sequence models:

1. **Baseline Models (`26_Machine_Learning.md`):** Gradient-Boosted Trees (XGBoost, LightGBM, CatBoost) to establish a fast, interpretable performance floor.
2. **Deep Sequence Models (`27_Deep_Learning.md`):** Recurrent architectures (LSTM, GRU) to capture long-term temporal dependencies in the light curves.
3. **Transformer Models (`28_Transformer_Models.md`):** State-of-the-art attention-based models (e.g., Temporal Fusion Transformers) for optimal performance.

## Lead-Time Reconciler

To empirically validate the models' predictive power, the **Lead-Time Reconciler** module continuously compares forecasted event probabilities against the *actual* events verified by the Nowcasting Engine (`22_Nowcasting.md`).
- Metric: `predicted_trigger_ts` vs `actual_peak_ts`.
- Goal: Quantify and track the true early-warning time provided by the combined HEL1OS/SoLEXS data.

## Training and Evaluation Strategy

- **Training Labels:** Provided exclusively by the historical Master Flare Catalogue generated in Phase 3.
- **Data Splitting:** Chronological split (not random) to prevent data leakage in time-series validation.
- **Metrics:** Precision, Recall, F1-Score, Brier Score (for probability calibration), and empirical lead time.

## Output Contract

The Forecasting Engine persists its predictions to the database (`30_Database_Design.md`) and exposes them via the Serving Layer (`32_API_Design.md`) for consumption by the Dashboard (`39_Dashboard.md`).

**Next document:** `24_CLI.md`
