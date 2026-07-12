# 29_Explainable_AI.md

**HeliosAI** — AI-Powered Space Weather Intelligence Platform
Document 29 of 61

---

## 1. Purpose

This document defines the Explainable AI (XAI) methodology used to interpret the predictions made by the HeliosAI forecasting models. Space weather forecasting requires high scientific accountability; black-box predictions are insufficient for satellite operators and power grid managers who must understand *why* a flare is being predicted before taking defensive action.

---

## 2. Methodology

The primary forecasting engine in HeliosAI is an XGBoost classifier (see `23_Forecasting.md`). To provide real-time explanations with minimal latency, we use a hybrid XAI approach:

### 2.1 Real-Time Approximation (Production)
In the production streaming pipeline (`src/pipeline/realtime_simulator.py`), evaluating full SHAP (SHapley Additive exPlanations) values for every rolling window step introduces unacceptable latency. Instead, we compute a localized feature contribution proxy:

`Feature Contribution = Global Feature Importance * Current Feature Value`

This allows us to instantly surface the "Top 3 Prediction Drivers" (e.g., `solexs_flux_max_60s`, `helios_flux_diff_60s`) in the API response and on the live dashboard.

### 2.2 Deep Analysis (Offline/Batch)
For post-event analysis and model debugging, we use TreeSHAP.
- **SHAP Summary Plots**: To understand the global impact of features across all historical flares.
- **SHAP Force Plots**: To break down individual false-positive or false-negative predictions during model retraining.

---

## 3. API Contract

The XAI insights are exposed via the `FeatureResponse` in `src/serving/api/main.py`:

```json
{
  "timestamp": "2024-01-01T12:00:00Z",
  "solexs_flux": 5.4e-6,
  "hel1os_flux": 2.1e-7,
  "forecast_probability": 0.85,
  "xai_top_features": "[\"solexs_flux_diff_60s\", \"helios_flux_max_60s\", \"hardness_ratio\"]",
  "data_quality_flag": "VALIDATED"
}
```

---

## 4. Interfaces to Other Documents
- **Depends on:** `23_Forecasting.md` (which defines the XGBoost model).
- **Referenced by:** `38_UI_UX.md`, `40_Data_Visualization.md`, `48_Model_Evaluation.md`, `59_Research_Paper.md`.
