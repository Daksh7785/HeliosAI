# 25 — Dashboard Overview

> **Document 25 of 61** in the HeliosAI documentation set (see `README.md` → Repository Structure). Provides a high-level overview of the web dashboard.

---

## Table of Contents

1. [Purpose of This Document](#purpose-of-this-document)
2. [Dashboard Objectives](#dashboard-objectives)
3. [Core Views](#core-views)
4. [Integration with API](#integration-with-api)

---

## Purpose of This Document

This document introduces the primary user interface for HeliosAI. It sets the stage for the deeper architectural documents (`37_Frontend_Architecture.md` through `41_Admin_Panel.md`).

## Dashboard Objectives

The dashboard is designed to provide operational personnel with an intuitive, real-time view of space weather conditions based on SoLEXS and HEL1OS data.
Key goals:
- **Real-time visibility:** Live updating light curves.
- **Alerting:** Immediate visual feedback when a flare is nowcasted or forecasted.
- **Explainability:** Interactive visualizations of model feature importance.

## Core Views

1. **Lightcurve View:** Interactive Plotly charts showing synchronized Soft and Hard X-ray fluxes.
2. **Catalogue Explorer:** A searchable, sortable data table of historical and recently nowcasted events.
3. **Forecast Console:** Gauge charts and probability timelines for 15m, 30m, and 60m horizons.
4. **Explainability Dashboard:** SHAP/Captum plots corresponding to specific forecasts.

## Integration with API

The dashboard acts as a pure client, containing no business logic or database connections. It consumes data exclusively through the REST API (`32_API_Design.md`) and receives real-time updates via WebSockets (`33_WebSocket_System.md`).

**Next document:** `26_Machine_Learning.md`
