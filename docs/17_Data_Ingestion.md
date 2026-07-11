# 17 — Data Ingestion

> **Document 17 of 61** in the HeliosAI documentation set (see `README.md` → Repository Structure). Resumes the architectural deep-dive after the domain and payload context established in `13`–`16`. Details how raw payload data enters the HeliosAI pipeline. Precedes `18_Data_Preprocessing.md`.

---

## Table of Contents

1. [Purpose of This Document](#purpose-of-this-document)
2. [Ingestion Architecture Overview](#ingestion-architecture-overview)
3. [Supported Data Formats](#supported-data-formats)
4. [Manual-Drop vs. Automated Ingestion](#manual-drop-vs-automated-ingestion)
5. [Handling Gaps and Corruptions](#handling-gaps-and-corruptions)
6. [Relevance to Downstream Modules](#relevance-to-downstream-modules)
7. [Revision History](#revision-history)

---

## Purpose of This Document

This document defines the boundaries, responsibilities, and constraints of the **Data Ingestion Layer** (part of the Phase 1 foundations). It explains how raw observational data from SoLEXS and HEL1OS is acquired, verified, and normalized before any scientific preprocessing or feature engineering occurs.

---

## Ingestion Architecture Overview

The Ingestion Layer is the single entry point for all external data entering HeliosAI. Its responsibilities are strictly limited to:
1. **Acquisition:** Reading data from disk (manual drop) or external APIs (e.g., GOES supplementary data).
2. **Parsing:** Extracting light curves, timestamps, and metadata from scientific formats (FITS, CDF) or tabular exports (CSV).
3. **Validation:** Running basic integrity checks (e.g., ensuring timestamps are monotonic, checking for outright corrupted files).
4. **Standardization:** Outputting a uniform, in-memory representation (typically pandas DataFrames or xarray Datasets) to hand off to the Preprocessing Layer.

The Ingestion Layer **does not** perform background subtraction, cross-band time synchronization, or feature engineering. Those are the domain of `18_Data_Preprocessing.md` and `21_Feature_Engineering.md`.

---

## Supported Data Formats

Because Aditya-L1 Level-1 data distribution formats can vary by payload or export method (via ISSDC PRADAN), the Ingestion Layer supports multiple format parsers:

- **FITS (Flexible Image Transport System):** The standard astronomical data format. The ingestion layer utilizes `astropy.io.fits` to extract binary table extensions containing time and flux columns, as well as crucial header metadata (e.g., observation start times, instrument modes).
- **CDF (Common Data Format):** Frequently used for space plasma and heliospheric data. Parsed using `cdflib` or `xarray`, extracting multidimensional arrays and epoch metadata.
- **CSV/Tabular:** Supported as a fallback or for simplified exports, requiring explicit column-mapping schemas to ensure timestamp and flux columns are correctly identified.

---

## Manual-Drop vs. Automated Ingestion

As established in `14_AdityaL1_Mission.md`, access to ISRO's PRADAN portal is often session-gated. Therefore, HeliosAI treats **Manual-Drop** as a first-class ingestion path, not just a temporary fallback.

1. **Watchdog / Manual-Drop:** A designated local directory (e.g., `/data/raw/`) is continuously monitored by a watchdog process. When a researcher drops a new FITS/CDF file into the directory, the ingestion pipeline automatically triggers.
2. **Automated API Pulls:** For supplementary, open-access data (such as NOAA GOES XRS), the ingestion layer contains scheduled workers that poll external REST APIs to fetch the latest observations, ensuring the reference datasets are continuously updated.

---

## Handling Gaps and Corruptions

Data gaps are inevitable due to ground-station contact loss, telemetry drops, or instrument anomalies. The Ingestion Layer's role is to **identify and flag** these issues, not to silently fix them.

- **Non-Monotonic Timestamps:** Automatically flagged. The ingestion parser enforces strictly increasing time arrays.
- **Corrupted Files:** Files that fail FITS/CDF header validation are quarantined in a `/data/error/` directory, and an alert is logged to the system.
- **Missing Data (NaNs):** Blocks of missing telemetry are preserved as `NaN` values in the standardized output. The decision on how to handle them (e.g., interpolation vs. dropping) is delegated to the Preprocessing Layer, which has the scientific context to make that choice.

---

## Relevance to Downstream Modules

| HeliosAI Component | Dependency on Ingestion Layer |
|---|---|
| Preprocessing Layer (`18_Data_Preprocessing.md`) | Relies on the uniform data structure output by Ingestion to apply calibration and time-sync logic without worrying about the original file format. |
| Raw-Data Validator (Phase 1) | The validation checks embedded in the ingestion parsers *are* the first line of defense in Phase 1. |
| Experience Layer (`24_CLI.md` / `25_Dashboard.md`) | The ingestion watchdog enables the "live" feel of the dashboard — dropping a file immediately updates the UI's real-time views. |

**Next document:** `18_Data_Preprocessing.md` — say **NEXT** to continue.

---

## Revision History

| Version | Date | Author | Notes |
|---|---|---|---|
| 0.1 | 2026-07-12 | HeliosAI Documentation (Antigravity workflow) | Initial Data Ingestion document — formats, drop vs. automated, and gap handling detailed |
