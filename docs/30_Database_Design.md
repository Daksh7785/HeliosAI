# 30 — Database Design

> **Document 30 of 61** in the HeliosAI documentation set (see `README.md` → Repository Structure). Defines the persistence layer for all HeliosAI subsystems.

---

## Table of Contents

1. [Purpose of This Document](#purpose-of-this-document)
2. [Database Technology Choice](#database-technology-choice)
3. [Schema Overview](#schema-overview)
4. [Time-Series Optimization](#time-series-optimization)
5. [Data Retention and Cleanup](#data-retention-and-cleanup)

---

## Purpose of This Document

This document defines the schema and technology behind the `shared/db/` module. It serves as the single source of truth for how HeliosAI persists raw light curves, processed features, event catalogues, and predictive model outputs.

## Database Technology Choice

- **Primary Database:** PostgreSQL with the TimescaleDB extension.
- **Why TimescaleDB?** HeliosAI deals with continuous high-frequency data (1-second cadence) from two payloads. TimescaleDB provides native hypertables, fast time-bucket aggregations, and automatic data retention policies, while remaining fully compatible with standard PostgreSQL tooling (SQLAlchemy, Alembic).
- **Cache / Broker:** Redis (used for Celery task queuing and WebSocket real-time data broadcasting).

## Schema Overview

The database is divided into logical domains:

1. **Raw Data (`raw_light_curve.py`):** Unaltered SoLEXS and HEL1OS observations directly out of the ingestion pipeline.
2. **Processed Data (`processed_light_curve.py`, `engineered_features.py`):** Background-subtracted, time-synchronized UTC light curves and their derived feature vectors (hardness ratio, gradients).
3. **Event Data (`flare_catalogue.py`):** The Master Catalogue populated by the Nowcasting Engine (`22_Nowcasting.md`). Contains start, peak, end times, classes, and cross-band confidence flags.
4. **Forecast Data (`forecast_events.py`):** Probability timelines output by the Forecasting Engine (`23_Forecasting.md`).
5. **System Data (`users.py`, `alerts.py`):** For the Dashboard and Serving Layer to manage access and alert thresholds.

## Time-Series Optimization

- All light curve and feature tables are converted into **TimescaleDB Hypertables** partitioned by the `timestamp` column.
- Continuous aggregates are used to rapidly serve downsampled data (e.g., 1-minute or 5-minute averages) to the Dashboard (`39_Dashboard.md`) to prevent browser memory exhaustion.

## Data Retention and Cleanup

Given the volume of continuous 1-second cadence data, raw tables have an automated retention policy dropping chunks older than 90 days. The Flare Catalogue and Forecast tables are retained indefinitely.

**Next document:** `31_Backend_Architecture.md`
