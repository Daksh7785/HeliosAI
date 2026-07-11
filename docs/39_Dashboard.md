# 39 — Dashboard Implementation

> **Document 39 of 61** in the HeliosAI documentation set (see `README.md` → Repository Structure). Details the main view of the Experience Layer.

---

## Table of Contents

1. [Purpose of This Document](#purpose-of-this-document)
2. [Layout Definition](#layout-definition)
3. [Live Telemetry Integration](#live-telemetry-integration)

---

## Purpose of This Document

This document focuses on the implementation details of the primary `/dashboard` route where operators spend most of their time.

## Layout Definition

The layout comprises:
1. **Top Navbar:** Contains the global timestamp (UTC), active system status (Ingestion Healthy/Degraded), and User Profile/Logout.
2. **Left Sidebar:** Navigation links (Dashboard, Catalogue, Explanations, Admin).
3. **Main Content Area:** 
   - **Upper Half:** The dual-axis Plotly graph showing the last 6 hours of fused SoLEXS/HEL1OS data.
   - **Lower Half:** A split view showing the Forecasting probability gauges (left) and a rolling log of recent Nowcast detections (right).

## Live Telemetry Integration

The Dashboard uses the `dash-extensions` library to establish a WebSocket connection directly to `services/api/` (`33_WebSocket_System.md`). When the `channel:telemetry:fused` topic emits new data, a client-side callback appends the new points to the Plotly figure without requiring a full page refresh, achieving true 1-second real-time visualization.

**Next document:** `40_Data_Visualization.md`
