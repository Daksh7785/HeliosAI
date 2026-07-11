# 21 — Feature Engineering

> **Document 21 of 61** in the HeliosAI documentation set (see `README.md` → Repository Structure). Concludes Phase 2 processing by transforming the instantaneous, aligned data from `20_Cross_Band_Fusion.md` into the rich temporal feature matrix required by the ML models in Phase 3 and 4. Precedes `22_Nowcasting.md`.

---

## Table of Contents

1. [Purpose of This Document](#purpose-of-this-document)
2. [Why Feature Engineering is Necessary](#why-feature-engineering-is-necessary)
3. [Temporal Derivatives (Momentum and Acceleration)](#temporal-derivatives-momentum-and-acceleration)
4. [Rolling Statistics and Volatility](#rolling-statistics-and-volatility)
5. [Domain-Specific Features (Fluence & Neupert Lag)](#domain-specific-features-fluence--neupert-lag)
6. [Feature Matrix Schema](#feature-matrix-schema)
7. [Revision History](#revision-history)

---

## Purpose of This Document

This document defines the **Feature Engineering Engine**. While `20_Cross_Band_Fusion.md` produced a clean, instantaneous snapshot of the solar atmosphere (Soft Flux, Hard Flux, Hardness Ratio), ML models — particularly sequence models and decision trees — require explicit temporal context. This module builds that context.

---

## Why Feature Engineering is Necessary

A single instantaneous spike in the Hardness Ratio is not enough to confidently predict an X-class flare. The system must know:
- Is the spike accelerating?
- How long has the baseline been elevated?
- What is the accumulated energy over the last hour?

Feature engineering transforms the `(t)` state into a `(t - w, t)` historical representation, mapping the raw physics to mathematically stable inputs for the intelligence layer.

---

## Temporal Derivatives (Momentum and Acceleration)

To capture the dynamics of the flare trigger, HeliosAI calculates the first and second derivatives of the core metrics.

- **First Derivative (Momentum):** Measures the rate of change. A rapidly rising Hardness Ratio `d(HR)/dt > 0` is the primary leading indicator of the impulsive phase.
- **Second Derivative (Acceleration):** Measures whether the growth is exponential. A positive acceleration in SoLEXS flux indicates the thermal heating phase is compounding.

These derivatives are calculated using finite difference methods over short rolling windows (e.g., 1 to 5 minutes) to smooth out micro-fluctuations.

---

## Rolling Statistics and Volatility

To provide the models with short-, medium-, and long-term context, HeliosAI computes rolling statistics over multiple time windows (e.g., `5m`, `15m`, `60m`, `6h`).

- **Rolling Mean:** Establishes the recent baseline, helping models distinguish between a quiet sun anomaly and an active region eruption.
- **Rolling Variance / Volatility:** Measures the "noisiness" of the signal. High volatility in the HEL1OS band often precedes structured particle acceleration.
- **Rolling Maximums:** Captures the peak intensity reached within the window, providing a memory of recent micro-flares.

---

## Domain-Specific Features (Fluence & Neupert Lag)

HeliosAI incorporates features derived directly from heliophysics:

- **Integrated Flux (Fluence):** The cumulative sum of the Soft X-ray flux over a defined window. Fluence is directly correlated with the total thermal energy deposited into the Earth's ionosphere (crucial for predicting radio blackouts).
- **Neupert Lag:** An advanced feature that attempts to quantify the time delay between the peak of the Hardness Ratio and the corresponding rise in Soft X-ray flux. A tightening lag can indicate a highly efficient particle acceleration mechanism, often seen in major eruptive flares.

---

## Feature Matrix Schema

The output of the Feature Engineering layer is the final **Feature Matrix**. For every synchronized timestamp `t`, the matrix contains:

1. `timestamp`
2. `solexs_flux`, `hel1os_flux`, `hardness_ratio` (Base Features)
3. `solexs_deriv1`, `hel1os_deriv1`, `hr_deriv1` (Momentum)
4. `solexs_deriv2`, `hel1os_deriv2`, `hr_deriv2` (Acceleration)
5. `hr_roll_mean_15m`, `solexs_roll_var_60m`, etc. (Rolling Stats)
6. `solexs_fluence_1h`, `neupert_lag_estimate` (Domain Features)

This wide matrix is the strict input contract for both the Nowcasting (`22`) and Forecasting (`23`) models.

---

## Revision History

| Version | Date | Author | Notes |
|---|---|---|---|
| 0.1 | 2026-07-12 | HeliosAI Documentation (Antigravity workflow) | Initial Feature Engineering document — derivatives, rolling stats, and domain features specified |
