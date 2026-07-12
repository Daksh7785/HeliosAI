# 23 — Forecasting

**HeliosAI** — AI-Powered Space Weather Intelligence Platform
Document 23 of 61

---

## 1. Purpose
Defines the predictive algorithmic methodology for forecasting solar flares prior to onset, resolving the P0-4 blocker.

---

## 2. Predictive Modelling
The forecasting engine relies on a trained XGBoost Classifier to predict the likelihood of a flare occurring within a specified lead time (e.g., the next 15 minutes).

### 2.1 Feature Engineering
The model operates on a trailing window of statistical features derived from both X-ray bands:
- Rolling means and standard deviations (characterizing local flux distribution).
- Rolling maximums (detecting recent micro-peaks).
- Finite differences over the window (characterizing the slope/rate-of-change).

### 2.2 Target Definition
- **Positive Class**: Timesteps falling strictly within the `lead_time_minutes` window *prior* to a true flare onset.
- **Negative Class**: Quiet background periods.
- **Exclusion**: Actual active flare periods are omitted from the training set to force the model to learn precursor patterns rather than active flare characteristics.

---

## 3. Evaluation
Metrics focus on high True Positive Rate (TPR) and low False Alarm Rate (FAR) for predictions, as specified by the PS-15 evaluation criteria.

**Next document:** `24_AI_Architecture.md` — say **NEXT** to continue.
