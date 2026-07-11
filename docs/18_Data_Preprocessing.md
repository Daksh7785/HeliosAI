# 18 — Data Preprocessing

> **Document 18 of 61** in the HeliosAI documentation set (see `README.md` → Repository Structure). Explains the critical translation from raw, isolated payload telemetry (output by `17_Data_Ingestion.md`) into a clean, scientifically calibrated time series. Precedes `19_Data_Synchronization.md` and `21_Feature_Engineering.md`.

---

## Table of Contents

1. [Purpose of This Document](#purpose-of-this-document)
2. [Preprocessing Architecture Overview](#preprocessing-architecture-overview)
3. [Time Synchronization (Spacecraft to UTC)](#time-synchronization-spacecraft-to-utc)
4. [Background Subtraction](#background-subtraction)
5. [Calibration and Flux Mapping](#calibration-and-flux-mapping)
6. [Gap Interpolation and Trajectory Splitting](#gap-interpolation-and-trajectory-splitting)
7. [Relevance to Downstream Modules](#relevance-to-downstream-modules)
8. [Revision History](#revision-history)

---

## Purpose of This Document

This document defines the responsibilities of the **Data Preprocessing Layer** (Phase 2). It outlines how HeliosAI handles the physical and instrumental realities of spacecraft data—background noise, clock drift, and calibration—ensuring that downstream Machine Learning models are fed a pure signal rather than instrumental artifacts.

---

## Preprocessing Architecture Overview

While the Ingestion Layer (`17`) is concerned with file formats (FITS, CDF), the Preprocessing Layer operates entirely on standardized, in-memory Pandas or xarray objects. 

Its pipeline executes in a strict sequence:
1. **Time Synchronization:** Convert raw spacecraft epoch times to standard UTC.
2. **Background Subtraction:** Estimate and remove the quiescent solar and instrumental background flux.
3. **Calibration:** Apply payload-specific response matrices to convert raw counts to physical flux, mapping SoLEXS to GOES-equivalent ranges.
4. **Data Gap Handling:** Interpolate minor telemetry drops or split the stream if large gaps render the sequence invalid for ML.

---

## Time Synchronization (Spacecraft to UTC)

Aditya-L1's payloads operate on an internal spacecraft clock. HeliosAI does not assume this clock perfectly matches Earth UTC.

- **Epoch Conversion:** Preprocessing extracts the time offset metadata embedded in the Level-1 files to convert spacecraft epochs to UTC timestamps.
- **Why this matters:** When HeliosAI eventually aligns SoLEXS soft X-ray data with HEL1OS hard X-ray data in the Fusion Layer (`19`), or validates against NOAA GOES supplementary data, all signals must share a perfectly aligned universal timeline to calculate the Hardness Ratio accurately.

---

## Background Subtraction

Raw flux measured by SoLEXS and HEL1OS includes both the active flare signal and a varying baseline consisting of quiescent solar emission, cosmic ray hits, and detector noise.

- **Dynamic Baselines:** HeliosAI calculates a dynamic baseline (e.g., using a rolling minimum over a long trailing window, or an asymmetrical least-squares fit) to track the background flux.
- **Subtraction:** This baseline is subtracted from the raw signal. The resulting "background-subtracted flux" ensures that HeliosAI detects flares based on relative energy release, not absolute background drift. 

---

## Calibration and Flux Mapping

To evaluate detections against the established operational standard (NOAA GOES A/B/C/M/X classes), SoLEXS data must be calibrated.

- **Physical Units:** Level-1 data is converted from raw detector counts to standard physical flux units (Watts per square meter, W/m²).
- **GOES-Equivalent Mapping:** The preprocessing layer applies an empirically derived mapping function to ensure the 1–15 keV SoLEXS thermal measurements translate accurately into the traditional 1–8 Ångström GOES classification thresholds. 

---

## Gap Interpolation and Trajectory Splitting

The Ingestion layer merely *flags* gaps as NaNs. Preprocessing must resolve them.

- **Short Gaps (e.g., < 1 minute):** HeliosAI employs linear or spline interpolation to fill minor missing segments, preserving the continuity required by the rolling-window feature engineering (`21`).
- **Long Gaps (e.g., > 1 minute):** Interpolation across large missing segments generates artificial, unphysical data. If a gap exceeds the acceptable threshold, the preprocessing layer splits the time series. The sequence model (`23_Forecasting.md`) treats the split as a hard boundary, effectively forcing the model state to reset rather than forecast across a blind spot.

---

## Relevance to Downstream Modules

| HeliosAI Component | Dependency on Preprocessing Layer |
|---|---|
| Cross-Band Fusion (`19_Data_Synchronization.md`) | Relies on the perfect UTC time mapping to align SoLEXS and HEL1OS. |
| Feature Engineering (`21_Feature_Engineering.md`) | Expects gap-free, background-subtracted flux trajectories to calculate derivatives and rolling statistics. |
| Nowcasting Engine (`22_Nowcasting.md`) | Depends on the physical calibration to correctly label a detection as an M-Class or X-Class flare. |

**Next document:** `19_Data_Synchronization.md` — say **NEXT** to continue.

---

## Revision History

| Version | Date | Author | Notes |
|---|---|---|---|
| 0.1 | 2026-07-12 | HeliosAI Documentation (Antigravity workflow) | Initial Data Preprocessing document — time sync, background modeling, and gap resolution defined |
