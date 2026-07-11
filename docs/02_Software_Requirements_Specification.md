# 02 — Software Requirements Specification (SRS)

**HeliosAI** — AI-Powered Space Weather Intelligence Platform
Document 02 of 61

---

## 1. Purpose

This document formally defines the functional and non-functional requirements for the HeliosAI platform. It translates the high-level goals from `01_Project_Vision.md` into concrete, testable engineering constraints.

---

## 2. User Personas

| Persona | Description | Primary Needs |
|---|---|---|
| **Space Weather Researcher** | Studies flare physics and precursors. | Access to raw features, reproducible model training, explainability metrics (SHAP). |
| **System Operator** | Monitors live solar activity. | Low-latency alerts, clear UI, low False Alarm Rate (FAR). |
| **Data Engineer** | Manages the ingestion pipeline. | Robust error handling for data gaps, clear telemetry, easy backfilling. |

---

## 3. Functional Requirements (FR)

### 3.1 Data Ingestion & Synchronization
- **FR-ING-01:** The system MUST ingest Level-1 FITS format light curves from SoLEXS and HEL1OS.
- **FR-ING-02:** The system MUST automatically resample and synchronize mismatched timestamps between the two instruments to a common temporal grid (e.g., 1-second cadence).
- **FR-ING-03:** The system MUST gracefully handle missing data (gaps up to N minutes) through interpolation or explicit `NaN` masking.

### 3.2 Nowcasting & Forecasting
- **FR-ML-01:** The system MUST classify active flares (Nowcasting) into GOES-equivalent classes (A, B, C, M, X) based on live flux levels.
- **FR-ML-02:** The system MUST output a probability forecast for flare occurrence within a parameterized future window (e.g., next 30, 60 minutes).
- **FR-ML-03:** A flare detection MUST require confirmation from both SoLEXS and HEL1OS channels (Dual-Band Fusion) to be marked as "Confirmed" in the master catalogue.
- **FR-ML-04:** Single-instrument detections MUST be recorded but flagged as "Tentative".

### 3.3 Dashboard & Alerting
- **FR-UI-01:** The system MUST provide a web-based dashboard displaying live fused light curves, current active flares, and forecast probabilities.
- **FR-UI-02:** The dashboard MUST update in near real-time via WebSockets as new data arrives.
- **FR-UI-03:** The system MUST dispatch alerts (e.g., via webhook or email) when a forecast probability exceeds a configurable threshold for M/X class flares.

### 3.4 Model Operations
- **FR-OPS-01:** The system MUST track all model training runs, hyperparameters, and evaluation metrics in a central registry (MLflow).
- **FR-OPS-02:** The system MUST link every generated forecast to the specific model version and data snapshot ID used to produce it.

---

## 4. Non-Functional Requirements (NFR)

### 4.1 Performance & Latency
- **NFR-PERF-01:** The end-to-end latency from data availability in the ingestion queue to an updated dashboard UI MUST NOT exceed 5 seconds.
- **NFR-PERF-02:** Model inference (both nowcasting and forecasting) MUST execute in under 500ms per timestamp.

### 4.2 Reliability & Availability
- **NFR-REL-01:** The system MUST recover automatically from transient database or message broker disconnects without data loss (via at-least-once Celery task retries).
- **NFR-REL-02:** Missing data from one instrument MUST NOT crash the processing pipeline; it must degrade to single-band operation smoothly.

### 4.3 Security & Auditing
- **NFR-SEC-01:** Admin-level endpoints (e.g., triggering manual model retraining) MUST require JWT-based authentication.
- **NFR-SEC-02:** No secrets, API keys, or database credentials SHALL be hardcoded in the repository.

### 4.4 Portability & Maintainability
- **NFR-PORT-01:** The entire platform MUST be deployable on a single host via `docker compose up --build`.
- **NFR-PORT-02:** The codebase MUST adhere strictly to Python typing (`mypy`) and formatting (`black`/`ruff`) standards.

---

## 5. Constraints

- **Language:** The platform is constrained to a 100% Python ecosystem (FastAPI, Dash, Celery, scikit-learn/PyTorch).
- **Data Volume:** Designed for the data rates of Aditya-L1; high-frequency magnetogram image processing is out of scope for Phase 1.

---

## 6. Interfaces to Other Documents

- **`03_System_Architecture.md`** — defines the components that satisfy these requirements.
- **`53_Testing.md`** — defines how these requirements are verified.
- **`48_Model_Evaluation.md`** — defines the specific success metrics for `FR-ML-01` and `FR-ML-02`.

---

## 7. Acceptance Criteria

- [ ] All requirements are uniquely identifiable (e.g., FR-ING-01).
- [ ] Requirements are testable and measurable, avoiding vague terms like "fast" or "reliable" without qualification.
- [ ] Requirements cleanly separate functional (what it does) from non-functional (how well it does it).

---

## 8. Review Checklist

- [ ] Ensure alignment with the Problem Statement 15 brief.
- [ ] Verify that dual-band fusion is explicitly required (FR-ML-03).

---

## 9. Future Improvements

- Add specific throughput requirements (events per second) if the system scales beyond single-spacecraft data.

---

## Antigravity Development Prompt

```
PROJECT CONTEXT:
You are implementing a documentation-only artifact — this task produces no source code.
Repository: HeliosAI. This is document 02 of a 61-document specification set.

FOLDER:
docs/02_Software_Requirements_Specification.md

FILES TO PRODUCE:
None (documentation task). Output exactly one file: docs/02_Software_Requirements_Specification.md

CODING STANDARDS:
N/A — Markdown only. Follow the structural template used by all other docs.

EXPECTED OUTPUT:
A single self-contained Markdown file capturing formal FRs and NFRs with unique IDs.

TESTING:
Documentation-only — validation is a Markdown lint pass.

ACCEPTANCE CRITERIA:
See §7 above.

DELIVERABLES:
docs/02_Software_Requirements_Specification.md

GIT COMMIT FORMAT:
docs: add 02_Software_Requirements_Specification.md (FRs and NFRs)
```

---

**Next document:** `03_System_Architecture.md` — say **NEXT** to continue.
