# 20 — Cross-Band Fusion

> **Document 20 of 61** in the HeliosAI documentation set (see `README.md` → Repository Structure). Explains the critical domain-specific operation that gives HeliosAI its predictive edge: combining SoLEXS and HEL1OS data. Precedes `21_Feature_Engineering.md`.

---

## Table of Contents

1. [Purpose of This Document](#purpose-of-this-document)
2. [The Physics Basis (The Neupert Effect)](#the-physics-basis-the-neupert-effect)
3. [Fusion Logic and The Hardness Ratio](#fusion-logic-and-the-hardness-ratio)
4. [Output: The Fused Record](#output-the-fused-record)
5. [Relevance to Downstream Modules](#relevance-to-downstream-modules)
6. [Revision History](#revision-history)

---

## Purpose of This Document

This document details the **Cross-Band Fusion** step within the Processing Subsystem. Now that data from both payloads has been preprocessed (`18`) and precisely aligned onto a common time base (`19`), HeliosAI fuses the Soft X-ray (SXR) and Hard X-ray (HXR) streams. This fusion is the primary differentiator between HeliosAI and legacy systems that rely solely on single-band data.

---

## The Physics Basis (The Neupert Effect)

HeliosAI's fusion approach is grounded in the **Neupert Effect**, a well-established empirical relationship in solar flare physics:

1. **The Precursor (HEL1OS):** During the impulsive phase of a flare, accelerated electrons slam into the dense solar chromosphere, emitting **Hard X-rays** via non-thermal bremsstrahlung. This energy release acts as an early warning or "precursor."
2. **The Main Phase (SoLEXS):** This electron bombardment rapidly heats the surrounding plasma, causing it to expand into the corona and emit **Soft X-rays** as thermal radiation. 

By monitoring both bands simultaneously, HeliosAI can detect the impulsive HXR spike (the trigger) *before* the SXR flux reaches its peak (the operational threat), granting the system crucial lead time for its forecasts.

---

## Fusion Logic and The Hardness Ratio

The fusion layer does not merely concatenate the two streams; it derives interaction metrics that expose the flare's underlying thermodynamic state.

The primary derived metric is the **Hardness Ratio**:
```text
Hardness Ratio (t) = HEL1OS HXR Flux (t) / SoLEXS SXR Flux (t)
```

**Why it matters:**
- A sharply rising Hardness Ratio indicates that non-thermal energy injection (particle acceleration) is dominating thermal emission — a strong leading indicator of an impending major flare.
- As the flare progresses and the plasma heats up, the SXR emission overwhelms the HXR emission, causing the Hardness Ratio to plummet.

The Fusion Layer calculates this ratio dynamically at every time step, along with running correlations between the two bands.

---

## Output: The Fused Record

The output of the Fusion Layer is a wide, multivariate feature vector representing the instantaneous state of the solar atmosphere at time `t`:

- `solexs_flux` (Thermal State)
- `hel1os_flux` (Non-Thermal State)
- `hardness_ratio` (Interaction Metric)
- `sync_quality_flag` (From the Synchronization Layer)

This vector is passed forward to `21_Feature_Engineering.md`, which will calculate the temporal derivatives (e.g., how fast the Hardness Ratio is changing over the last 5 minutes) required by the ML models.

---

## Relevance to Downstream Modules

| HeliosAI Component | Dependency on Fusion |
|---|---|
| Feature Engineering (`21_Feature_Engineering.md`) | Requires the derived `hardness_ratio` to compute momentum and volatility features. |
| Forecasting Engine (`23_Forecasting.md`) | Relies on the early-warning HXR precursor exposed by the fusion layer to achieve its >24-hour prediction horizons. |
| Experience Layer (`24_CLI.md` / `25_Dashboard.md`) | Visualizes the Soft vs. Hard X-ray light curves and the Hardness Ratio side-by-side to explain predictions to human operators. |

**Next document:** `21_Feature_Engineering.md` — say **NEXT** to continue.

---

## Revision History

| Version | Date | Author | Notes |
|---|---|---|---|
| 0.1 | 2026-07-12 | HeliosAI Documentation (Antigravity workflow) | Initial Cross-Band Fusion document — Neupert Effect and Hardness Ratio logic defined |
