# 18_Data_Preprocessing.md

**HeliosAI** — AI-Powered Space Weather Intelligence Platform
Document 18 of 61

---

## 1. Purpose

This document outlines the data preprocessing pipeline for raw telemetry received from Aditya-L1's SoLEXS and HEL1OS instruments. Because space-based sensors are subject to cosmic ray hits, thermal noise, and telemetry dropouts, robust data cleaning and state management is required before the data reaches the forecasting models.

---

## 2. Telemetry State Machine

All incoming data points are tracked using a `data_quality_flag`. The state machine operates as follows:

1. **RAW**: Initial state upon ingestion.
2. **VALIDATED**: The data point passes physical bounds checks (e.g., non-negative flux, within expected orders of magnitude for solar X-rays).
3. **QUARANTINED**: The data point is physically impossible (e.g., negative flux values) or represents a statistically impossible spike (e.g., > 5-sigma jump in 1 second) indicative of a cosmic ray hit on the CCD rather than a solar event.
4. **IMPUTED**: (Optional state if downstream systems request gap-filled data). Quarantined points are replaced using forward-filling or linear interpolation based on the preceding 60 seconds of valid data.

---

## 3. Implementation

The preprocessing logic is centralized in `src/data_loader.py`.

### 3.1 Rules for Quarantining
- **Negative Values**: `if flux < 0: flag = QUARANTINED`
- **Missing Timestamps**: Gaps larger than the 1-second cadence trigger gap-detection flags.

### 3.2 Feature Engineering
Once data is `VALIDATED` (or `IMPUTED`), rolling window features are generated (see `19_Feature_Engineering.md`):
- Rolling maxima/minima (60s, 5m).
- 1st and 2nd derivatives of flux.
- Cross-instrument ratios (e.g., HEL1OS/SoLEXS Hardness Ratio).

---

## 4. Interfaces to Other Documents
- **Depends on:** `12_Aditya_L1_Payloads.md` (for expected flux ranges).
- **Referenced by:** `19_Feature_Engineering.md`, `29_Explainable_AI.md`, `32_API_Design.md`.
