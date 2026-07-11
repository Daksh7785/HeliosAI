# 22 — Nowcasting Engine

> **Document 22 of 61** in the HeliosAI documentation set (see `README.md` → Repository Structure). Defines Phase 3 of the system, consuming the fused feature vector from `21_Feature_Engineering.md` and feeding into `23_Forecasting.md` and `30_Database_Design.md`.

---

## Table of Contents

1. [Purpose of This Document](#purpose-of-this-document)
2. [What is Nowcasting in HeliosAI?](#what-is-nowcasting-in-heliosai)
3. [Detector Architecture](#detector-architecture)
4. [Cross-Band Fusion Gate](#cross-band-fusion-gate)
5. [Flare Class Assignment](#flare-class-assignment)
6. [Master Catalogue Promotion](#master-catalogue-promotion)
7. [Testing and Validation](#testing-and-validation)

---

## Purpose of This Document

This document describes the **Nowcasting Engine**, which serves as the real-time event detection layer. While the feature engineering layer transforms light curves, the nowcasting engine translates those features into discrete, actionable solar flare events.

## What is Nowcasting in HeliosAI?

Nowcasting refers to the detection of a flare *as it happens* or *immediately after it begins*. In HeliosAI, this involves:
- Rapid threshold and changepoint detection.
- Peak, rise, and decay phase estimation.
- Assignment of standard flare classes (A, B, C, M, X).
- Producing a labeled event catalogue used for downstream forecasting training.

## Detector Architecture

HeliosAI uses independent detectors for SoLEXS and HEL1OS before fusing the results:

1. **SoLEXS Detector:** Focuses on soft X-ray flux thresholds and gradients.
2. **HEL1OS Detector:** Focuses on hard X-ray impulsive spikes.

Both detectors utilize:
- **CUSUM (Cumulative Sum) algorithms** for rapid changepoint detection.
- **Dynamic Thresholding** based on the rolling background calculated in `18_Data_Preprocessing.md`.

## Cross-Band Fusion Gate

Detections from individual bands are passed through a Cross-Band Fusion Gate:
- **Confirmed Events:** Detected concurrently in both SoLEXS and HEL1OS (high confidence).
- **Tentative Events:** Detected only in SoLEXS (e.g., low-energy A/B class flares where hard X-ray emission is minimal).
- **Anomalies:** Detected only in HEL1OS without corresponding SoLEXS activity (often flagged as potential noise or particle hits).

## Flare Class Assignment

Flare classes are assigned strictly based on the GOES-equivalent soft X-ray peak flux measured by SoLEXS. The engine maps SoLEXS peak flux limits to the standard log-scale classes:
- A-class: < 10^-7 W/m^2
- B-class: 10^-7 to 10^-6 W/m^2
- C-class: 10^-6 to 10^-5 W/m^2
- M-class: 10^-5 to 10^-4 W/m^2
- X-class: >= 10^-4 W/m^2

## Master Catalogue Promotion

Once an event's decay phase concludes, the fully parameterized event (start, peak, end times, class, confidence) is promoted to the **Master Flare Catalogue** via the `services/intelligence/catalogue_builder/` module. This catalogue acts as the source of truth.

## Testing and Validation

The nowcasting engine will be validated against historical GOES XRS event catalogues to ensure precision and recall align with established solar benchmarks.

**Next document:** `23_Forecasting.md`
