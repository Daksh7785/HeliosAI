# 02 — Software Requirements Specification

**HeliosAI** — AI-Powered Space Weather Intelligence Platform
Document 02 of 61

---

## 1. Executive Summary

This is the formal SRS: functional and non-functional requirements, expressed as testable statements and user stories, derived directly from Problem Statement 15. Every later architecture and implementation document traces back to a requirement ID defined here.

---

## 2. Purpose

Provide a single, unambiguous, testable source of truth for *what* HeliosAI must do, independent of *how* (architecture) or *why* (vision, `01_Project_Vision.md`).

---

## 3. Scope

Covers functional requirements (FR), non-functional requirements (NFR), user stories, and requirement-level acceptance criteria. Does not cover system design (`03`–`05`) or data schema (`30_Database_Design.md`).

---

## 4. Requirement Numbering Convention

`FR-<subsystem>-<seq>` for functional, `NFR-<category>-<seq>` for non-functional. Every requirement ID is stable once published — later documents cite it, never restate it.

---

## 5. Functional Requirements

### 5.1 Ingestion (FR-ING)

| ID | Requirement |
|---|---|
| FR-ING-01 | System shall fetch SoLEXS and HEL1OS Level-1 data from ISSDC PRADAN, automated where token access is available, manual-drop otherwise |
| FR-ING-02 | System shall validate raw file integrity (checksum, expected schema) before processing |
| FR-ING-03 | System shall process incrementally — never reprocess full history on each run |

### 5.2 Processing (FR-PROC)

| ID | Requirement |
|---|---|
| FR-PROC-01 | System shall synchronize spacecraft time to UTC for both payloads |
| FR-PROC-02 | System shall perform background subtraction and noise filtering per payload |
| FR-PROC-03 | System shall compute engineered features including hardness ratio, flux gradient, rise/decay constants, wavelet energy |

### 5.3 Nowcasting (FR-NOW)

| ID | Requirement |
|---|---|
| FR-NOW-01 | System shall detect flare candidates independently in each band |
| FR-NOW-02 | System shall fuse per-band candidates into a master catalogue with confidence scoring |
| FR-NOW-03 | System shall flag single-band-only detections as tentative, never silently drop or silently confirm them |
| FR-NOW-04 | System shall assign a GOES-equivalent class (A/B/C/M/X) to each confirmed flare |

### 5.4 Forecasting (FR-FORE)

| ID | Requirement |
|---|---|
| FR-FORE-01 | System shall output the probability of a flare occurring within a configurable horizon N (15/30/60 min) |
| FR-FORE-02 | System shall log predicted trigger timestamp and, once resolved, actual peak timestamp, to compute lead time |
| FR-FORE-03 | System shall support multiple model families (gradient-boosted trees, LSTM/GRU, Transformer-family) behind a common interface |

### 5.5 Explainability (FR-XAI)

| ID | Requirement |
|---|---|
| FR-XAI-01 | System shall provide SHAP-based explanations for tree-model outputs |
| FR-XAI-02 | System shall provide attention/integrated-gradients explanations for deep-model outputs |

### 5.6 Serving & Dashboard (FR-SRV)

| ID | Requirement |
|---|---|
| FR-SRV-01 | System shall expose REST + WebSocket APIs for catalogue and live data access |
| FR-SRV-02 | System shall provide a dashboard visualizing dual-band light curves with synchronized time axes |
| FR-SRV-03 | System shall visually alert (banner) when a flare is nowcasted or forecasted |
| FR-SRV-04 | System shall support optional webhook/email alert delivery |

### 5.7 Access Control (FR-SEC)

| ID | Requirement |
|---|---|
| FR-SEC-01 | System shall authenticate all API access (no anonymous write access) |
| FR-SEC-02 | System shall enforce role-based permissions (viewer/analyst/ml_engineer/admin/service) |

---

## 6. Non-Functional Requirements

| ID | Category | Requirement |
|---|---|---|
| NFR-SCALE-01 | Scalability | Handle continuous multi-day, multi-cadence ingestion without full reprocessing |
| NFR-REL-01 | Reliability | Ingestion/processing jobs idempotent and resumable |
| NFR-LAT-01 | Latency | Nowcasting alerts generated within a documented bounded delay of data availability |
| NFR-AUD-01 | Auditability | Every catalogue entry and forecast traceable to model version + data snapshot |
| NFR-SEC-01 | Security | All endpoints authenticated; no hardcoded secrets |
| NFR-PORT-01 | Portability | Fully containerized, `docker compose up` reproducible |

---

## 7. User Stories

| ID | Story |
|---|---|
| US-01 | As a space-weather analyst, I want to see live dual-band light curves so that I can visually confirm an automated alert. |
| US-02 | As an ML engineer, I want every model version logged with its training data snapshot so that I can reproduce or roll back any production model. |
| US-03 | As an admin, I want to adjust alert thresholds and preview their historical impact before saving, so that I don't blindly degrade FAR. |
| US-04 | As a researcher, I want to export the master catalogue for a date range so that I can perform independent analysis. |
| US-05 | As a new contributor, I want a documented, containerized local setup so that I can start developing without manual environment archaeology. |

---

## 8. Requirement Traceability (sample)

| Requirement | Implemented/Detailed In |
|---|---|
| FR-NOW-02, FR-NOW-03 | `22_Nowcasting.md` |
| FR-FORE-01, FR-FORE-02 | `23_Forecasting.md`, `48_Model_Evaluation.md` |
| FR-SRV-02, FR-SRV-03 | `39_Dashboard.md`, `42_Alert_System.md` |
| FR-SEC-01, FR-SEC-02 | `35_Authentication.md`, `36_Authorization.md` |
| NFR-AUD-01 | `44_Logging.md`, `46_MLOps.md` |

Full traceability matrix (all IDs × all documents) is maintained as the documentation set closes out, in `MASTER_IMPLEMENTATION_GUIDE.md`.

---

## 9. Acceptance Criteria

- [ ] Every FR/NFR has a stable ID never renumbered after publication.
- [ ] Every FR/NFR is cited by at least one downstream document once that tier is written.
- [ ] No requirement is untestable (each is phrased as a verifiable "shall" statement).

---

## 10. Review Checklist

- [ ] No architecture/design leaked into requirement statements (kept to "what," not "how").
- [ ] User stories map to at least one FR each.

---

## 11. Future Improvements

- Add non-functional requirements for accessibility compliance level once `38_UI_UX.md`'s WCAG target is finalized in implementation.

---

## Antigravity Development Prompt

```
PROJECT CONTEXT:
HeliosAI — dual-band Aditya-L1 flare nowcasting/forecasting platform (ISRO PS-15).
Document 02 of 61: formal Software Requirements Specification.

FOLDER: docs/02_Software_Requirements_Specification.md

FILES TO PRODUCE: docs/02_Software_Requirements_Specification.md only.

CODING STANDARDS: Markdown; requirement IDs must follow the FR-<subsystem>-<seq> /
NFR-<category>-<seq> convention exactly, and IDs must never be renumbered once published
(later docs will cite them by ID).

EXPECTED OUTPUT: Complete FR/NFR tables per subsystem (Ingestion, Processing, Nowcasting,
Forecasting, Explainability, Serving, Access Control), user stories, and a traceability
sample table, matching the structure above.

EDGE CASES / VALIDATION: Every requirement must be phrased as a testable "shall" statement,
not an aspiration. Reject any requirement that cannot be objectively verified.

TESTING: Cross-reference audit — every FR/NFR ID must appear in at least one later document's
"Interfaces to Other Documents" or equivalent section once that document exists.

ACCEPTANCE CRITERIA: See §9 above.

DELIVERABLES: docs/02_Software_Requirements_Specification.md

GIT COMMIT FORMAT: docs: add 02_SRS.md (functional and non-functional requirements)
```

---

**Next document:** `03_System_Architecture.md` — say **NEXT** to continue.
