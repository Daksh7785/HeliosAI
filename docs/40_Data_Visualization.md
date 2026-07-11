# 40 — Data Visualization

> **Document 40 of 61** in the HeliosAI documentation set (see `README.md` → Repository Structure). Defines the specific charting requirements.

---

## Table of Contents

1. [Purpose of This Document](#purpose-of-this-document)
2. [Light Curve Plots](#light-curve-plots)
3. [Forecast Probability Plots](#forecast-probability-plots)
4. [Explainability Plots](#explainability-plots)

---

## Purpose of This Document

This document standardizes how Plotly is used to render HeliosAI's complex datasets within the Dash application.

## Light Curve Plots

The central visualization is a shared-X-axis (Time in UTC) dual-Y-axis line chart.
- **Left Y-Axis (Log Scale):** SoLEXS Soft X-ray flux (W/m^2). Crucial for displaying the 4-order-of-magnitude difference between background and X-class flares.
- **Right Y-Axis (Linear Scale):** HEL1OS Hard X-ray counts/sec. 
- **Overlays:** Vertical dashed lines indicating the Nowcasting Engine's start, peak, and end detections.

## Forecast Probability Plots

Represented as gauge charts or horizontal bar charts showing the probability [0-100%] of an M/X class flare occurring in the next 15, 30, and 60 minutes.

## Explainability Plots

SHAP summary plots are rendered as horizontal bar charts ranking features by impact. Captum integrated gradients are visualized as a heatmap ribbon aligned underneath the main light curve plot, visually connecting the "why" to the "when".

**Next document:** `41_Admin_Panel.md`
