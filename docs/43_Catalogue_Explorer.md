# 43 — Catalogue Explorer

> **Document 43 of 61** in the HeliosAI documentation set (see `README.md` → Repository Structure). Defines the retrospective analysis interface.

---

## Table of Contents

1. [Purpose of This Document](#purpose-of-this-document)
2. [Explorer Functionality](#explorer-functionality)
3. [Data Export](#data-export)
4. [Integration with Nowcasting](#integration-with-nowcasting)

---

## Purpose of This Document

The Catalogue Explorer is a dedicated view within the Dashboard (`39_Dashboard.md`) focused entirely on historical data analysis.

## Explorer Functionality

Rather than a live-scrolling light curve, the Catalogue Explorer presents the Master Flare Catalogue as a rich, filterable data grid (using AG Grid or Dash DataTable).
- **Filtering:** Filter by date range, GOES-class equivalent (e.g., show only >M1.0 flares), and cross-band confidence (confirmed vs. tentative).
- **Drill-Down:** Clicking a row opens a modal or navigates to a detailed view of that specific flare, loading the exact light curve segment and its corresponding Explainability artifacts (`29_Explainable_AI.md`).

## Data Export

Researchers require raw data for their own analyses. The explorer provides a "Download CSV" button that triggers a backend aggregation task, zipping the relevant processed light curve and feature engineered datasets for the selected events.

## Integration with Nowcasting

As soon as the Nowcasting Engine (`22_Nowcasting.md`) finalizes an event and promotes it to the database, the WebSocket system broadcasts an invalidation signal to the Catalogue Explorer, prompting it to seamlessly fetch the new row.

**Next document:** `44_MLOps.md`
