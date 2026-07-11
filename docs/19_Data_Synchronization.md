# 19 — Data Synchronization

> **Document 19 of 61** in the HeliosAI documentation set (see `README.md` → Repository Structure). Concludes the data preparation pipeline within the Processing Subsystem, following `18_Data_Preprocessing.md`. Details the crucial step of aligning the disparate soft and hard X-ray timelines before cross-band fusion. Precedes `20_Cross_Band_Fusion.md`.

---

## Table of Contents

1. [Purpose of This Document](#purpose-of-this-document)
2. [The Synchronization Problem](#the-synchronization-problem)
3. [Common Time Base (Resampling)](#common-time-base-resampling)
4. [Jitter and Latency Handling](#jitter-and-latency-handling)
5. [Output: The Synchronized Stream](#output-the-synchronized-stream)
6. [Relevance to Downstream Modules](#relevance-to-downstream-modules)
7. [Revision History](#revision-history)

---

## Purpose of This Document

This document outlines the **Data Synchronization Engine**'s design. After `18_Data_Preprocessing.md` cleans each instrument's data individually, this module aligns them onto a single, perfect timeline. This is a hard prerequisite for `20_Cross_Band_Fusion.md`, which calculates physical metrics (like the Hardness Ratio) that require simultaneous readings.

---

## The Synchronization Problem

SoLEXS and HEL1OS are independent payloads. They do not naturally produce telemetry arrays that align row-by-row:
- **Differing Cadences:** One instrument may record at 1-second intervals while the other records at 0.5-second or 2-second intervals, depending on the active observation mode.
- **Clock Drift:** Despite UTC conversions in the Preprocessing layer, micro-second jitters exist between the two instruments' recording triggers.
- **Asymmetric Data Drops:** A telemetry drop might affect HEL1OS for 5 seconds while SoLEXS continues transmitting perfectly.

HeliosAI's Machine Learning models expect a unified sequence where `time_step[t]` contains both soft and hard X-ray features exactly aligned.

---

## Common Time Base (Resampling)

To solve differing cadences and jitter, the Synchronization Engine resamples both clean data streams onto a rigid **Common Time Base**.

- **Target Frequency:** HeliosAI standardizes on a fixed cadence (e.g., exactly 1.0 seconds) for the Fusion layer. 
- **Aggregation Strategy:** 
  - For higher-cadence data (e.g., 0.5s), the engine aggregates values (usually taking the mean flux) to downsample to the 1-second bin.
  - For lower-cadence data, it uses linear interpolation (within strictly defined limits, per `18_Data_Preprocessing.md`) to upsample to the 1-second bin.
- **Anchor Point:** The time base is anchored to standard UTC boundaries (e.g., exact seconds like `14:02:00.000`), stripping out fractional-second recording offsets.

---

## Jitter and Latency Handling

When operating in **Nowcasting (Live) Mode** (`22_Nowcasting.md`), data arrives asynchronously. 

- **Buffer Windows:** The synchronization engine maintains a rolling buffer. It waits for a configured "latency window" (e.g., 30 seconds) to ensure data from both payloads for `time_step[t]` has arrived before emitting the synchronized row.
- **Asymmetric Dropouts:** If the buffer window expires and one payload's data is still missing (due to a ground-station dropout), the engine flags that timestamp as `PARTIAL_SYNC`. The downstream fusion layer is designed to handle `PARTIAL_SYNC` rows by falling back to single-band heuristics, preventing the entire pipeline from stalling due to one instrument.

---

## Output: The Synchronized Stream

The final output of this module is a unified, multi-variate time series (often represented as a merged Pandas DataFrame):
- `timestamp`: The exact UTC anchor.
- `solexs_flux`: The calibrated, background-subtracted soft X-ray flux.
- `hel1os_flux`: The calibrated, background-subtracted hard X-ray flux.
- `sync_quality_flag`: Indicates whether the row contains fully aligned data, interpolated data, or is missing one payload (`PARTIAL_SYNC`).

---

## Relevance to Downstream Modules

| HeliosAI Component | Dependency on Synchronization |
|---|---|
| Cross-Band Fusion (`20_Cross_Band_Fusion.md`) | Relies entirely on the `solexs_flux` and `hel1os_flux` being physically simultaneous to calculate ratios. |
| Feature Engineering (`21_Feature_Engineering.md`) | Needs a rigid, gapless, fixed-cadence timeline to calculate rolling derivatives cleanly. |
| Alert Dispatcher (Phase 5) | The latency introduced by the buffer window directly dictates the minimum possible delay for a live alert. |

**Next document:** `20_Cross_Band_Fusion.md` — say **NEXT** to continue.

---

## Revision History

| Version | Date | Author | Notes |
|---|---|---|---|
| 0.1 | 2026-07-12 | HeliosAI Documentation (Antigravity workflow) | Initial Data Synchronization document — common time base and buffer window defined |
