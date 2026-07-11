# 14 — Aditya-L1 Mission

> **Document 14 of 61** in the HeliosAI documentation set (see `README.md` → Repository Structure). Narrows from general space weather context (`13_Space_Weather.md`) to the specific mission HeliosAI's data originates from. Precedes `15_SoLEXS.md` and `16_HEL1OS.md`, which detail the two payloads individually.

---

## Table of Contents

1. [Purpose of This Document](#purpose-of-this-document)
2. [Mission Overview](#mission-overview)
3. [Why L1](#why-l1)
4. [Payload Suite](#payload-suite)
5. [Mission Timeline (Public Record)](#mission-timeline-public-record)
6. [Data Products and Access](#data-products-and-access)
7. [Relevance to HeliosAI](#relevance-to-heliosai)
8. [Known Constraints Affecting Ingestion Design](#known-constraints-affecting-ingestion-design)
9. [Revision History](#revision-history)

---

## Purpose of This Document

This document is a **mission-level reference** for contributors who need to understand Aditya-L1 as a spacecraft and data source before working with SoLEXS/HEL1OS data specifically (detailed next in `15` and `16`). Where mission details affect ingestion design decisions already made in `README.md` and `08_Development_Roadmap.md`, this document makes the connection explicit.

> **Note on sourcing:** Aditya-L1 is ISRO's first dedicated solar observation mission. Precise, current operational parameters (exact orbit insertion dates, payload health status, latest data release notes) should always be verified against ISRO/ISSDC's official mission pages before being relied upon for implementation, since mission status can change after this document was written. This document captures the mission's role and design rationale at an architectural level rather than asserting live operational figures.

---

## Mission Overview

Aditya-L1 is ISRO's first dedicated space-based solar observatory, designed to study the Sun continuously from a halo orbit around the Sun-Earth Lagrange Point 1 (L1), roughly 1.5 million km from Earth toward the Sun. The mission carries a suite of payloads observing the Sun across multiple regimes — from the photosphere and chromosphere through the corona, plus in-situ solar wind and particle measurements — of which **SoLEXS** and **HEL1OS** (HeliosAI's two data sources) are the X-ray-focused instruments.

The mission's stated scientific goals include understanding coronal heating, solar wind acceleration, coronal mass ejections, and flare dynamics — flare-related science being directly aligned with HeliosAI's own focus.

---

## Why L1

The Sun-Earth L1 point is a gravitationally balanced location where a spacecraft can maintain a stable halo orbit while keeping a **continuous, unobstructed view of the Sun**, free from Earth's shadow (eclipse) and atmospheric interference. This is the mission-level justification for the continuity advantage introduced in `13_Space_Weather.md` — an Earth-orbiting X-ray solar monitor would periodically lose solar view during eclipse seasons, introducing data gaps exactly when continuous flare monitoring matters most.

For HeliosAI, this means the underlying data stream is architecturally well-suited to a continuous nowcasting/forecasting pipeline (few structural gaps from orbital geometry), though **downlink cadence, ground-station contact windows, and processing latency** — not orbital position — are the practical factors that determine real-world data latency (see [Known Constraints](#known-constraints-affecting-ingestion-design) below).

---

## Payload Suite

Aditya-L1 carries multiple payloads; HeliosAI is scoped to use only the two relevant to X-ray flare monitoring:

| Payload | Domain | Relevance to HeliosAI |
|---|---|---|
| **SoLEXS** (Solar Low Energy X-ray Spectrometer) | Soft X-ray (~1–15 keV) | Primary soft X-ray input; thermal flare emission, GOES-comparable band |
| **HEL1OS** (High Energy L1 Orbiting X-ray Spectrometer) | Hard/high-energy X-ray | Primary hard X-ray input; non-thermal precursor signal |
| VELC, SUIT, ASPEX, PAPA, magnetometer, etc. | Coronagraphy, UV imaging, particle/field in-situ measurement | **Out of scope** for HeliosAI (per `README.md` → Scope); noted here only for mission-context completeness |

HeliosAI deliberately does not attempt to ingest the full Aditya-L1 payload suite — this is a scope decision, not a data-availability limitation, consistent with the Problem Statement's specific framing around SoLEXS + HEL1OS.

---

## Mission Timeline (Public Record)

At a high level, per ISRO's public mission record:

- Aditya-L1 launched from Sriharikota aboard a PSLV vehicle.
- It underwent a multi-phase Earth-bound orbit-raising sequence followed by a trans-Lagrangian-point injection.
- It achieved insertion into its halo orbit around L1 and began science operations.

**Implementation note:** exact dates and current mission phase/status should be confirmed against ISRO's official mission page at implementation time rather than hard-coded from this document, since this document intentionally avoids asserting specific dates that could go stale.

---

## Data Products and Access

- **Access point:** ISSDC's PRADAN (Payload data Repository, Analysis and Dissemination portal) is the designated public access point for Aditya-L1 Level-1 (and higher) data products, as already established in `README.md`.
- **Data levels:** Level-1 data (calibrated but not yet science-ready-fused) is HeliosAI's stated ingestion target, per `README.md` → Executive Summary — HeliosAI performs its own synchronization, calibration-aware cleaning, and feature engineering on top of L1 rather than depending on a higher processing level that may not always be promptly available.
- **Format:** Level-1 payload data is typically distributed in scientific data formats such as FITS or CDF (or CSV exports, depending on payload/portal conventions) — this is why `17_Data_Ingestion.md` scopes format parsing for FITS/CDF/CSV rather than assuming a single format.

---

## Relevance to HeliosAI

Every ingestion and processing design decision already made upstream traces back to a mission-level fact documented here:

| HeliosAI Design Decision | Mission Fact It Responds To |
|---|---|
| Manual-drop ingestion as a first-class path (not fallback) | PRADAN portal access is often session/credential-gated per user |
| Format parsers for FITS/CDF/CSV | Level-1 data distribution conventions vary by payload/portal export |
| Spacecraft-time → UTC synchronization engine | Payloads operate on onboard spacecraft clocks, not UTC directly |
| Continuous-ingestion, incremental-processing NFR (`README.md`) | L1 halo orbit gives near-continuous solar visibility, unlike Earth-orbiting eclipse-affected assets |
| GOES XRS as optional supplementary/cross-validation data | Provides an independently operated, long-running reference dataset for calibration/labeling confidence |

---

## Known Constraints Affecting Ingestion Design

- **Ground contact/downlink cadence** determines real-world data latency more than orbital position does — a nowcasting system's practical alert latency is bounded below by this, not by algorithm speed alone. This is directly relevant to the Latency NFR in `README.md`, whose exact target is deferred to `45_Monitoring.md`.
- **Payload commissioning/calibration status** can affect data quality windows early in a mission's life; HeliosAI's raw-data validator (Phase 1, per `08_Development_Roadmap.md`) is designed to flag and quarantine anomalous segments rather than assume uniform data quality across the mission's full history.
- **Portal access tier variability** (already discussed) remains the top-scored risk in `10_Risk_Assessment.md` (R1) and should be re-verified against ISSDC PRADAN's current access policy before Phase 1 implementation begins.

---

## Revision History

| Version | Date | Author | Notes |
|---|---|---|---|
| 0.1 | 2026-07-12 | HeliosAI Documentation (Antigravity workflow) | Initial Aditya-L1 Mission document — mission overview, L1 rationale, payload suite, and data-access constraints established |
