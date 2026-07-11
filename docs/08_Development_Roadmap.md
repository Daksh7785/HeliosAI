# 08 — Development Roadmap

**HeliosAI** — AI-Powered Space Weather Intelligence Platform
Document 08 of 61

---

## 1. Executive Summary

This document translates the requirements from `02_Software_Requirements_Specification.md` and the architecture from `03_System_Architecture.md` into a sequenced delivery plan. It defines what constitutes a Minimum Viable Product (MVP) and the subsequent phases leading to the final hackathon submission.

---

## 2. Purpose

Provide a clear sequence of implementation phases. This ensures the team builds end-to-end vertical slices of functionality rather than isolated components that cannot be integrated until the final week.

---

## 3. Scope

Defines the sequence of feature development, milestones, and MVP definition. Excludes specific dates (see `09_Project_Timeline.md`) and task assignments.

---

## 4. Phase 1: Foundation (Sprint 1)

**Goal:** Establish the repository, core infrastructure, and data ingestion pipeline.

*   **Deliverables:**
    *   Docker Compose environment (`postgres`, `timescaledb`, `redis`).
    *   Basic FastAPI application skeleton.
    *   Database migrations (Alembic) for core tables (`raw_telemetry`).
    *   Scripts to download and parse historical SoLEXS and HEL1OS data (FR-ING-01).
*   **Success Criteria:** Can run `docker compose up` and successfully execute a script that populates the local database with a sample of raw ISRO data.

---

## 5. Phase 2: Processing & Baseline Intelligence (Sprint 2) - **MVP**

**Goal:** Establish the end-to-end data flow and a baseline, single-band detection mechanism.

*   **Deliverables:**
    *   Time-synchronization logic (FR-PROC-01).
    *   Basic feature engineering (FR-PROC-03).
    *   Baseline Nowcasting Engine (rule-based or simple thresholding on single bands) (FR-NOW-01).
    *   Basic API endpoints to query the master catalogue.
*   **Success Criteria (MVP):** The system ingests raw data, processes it, detects basic flare events using a simple heuristic, and serves those events via a REST API.

---

## 6. Phase 3: Advanced Intelligence & Fusion (Sprint 3)

**Goal:** Implement dual-band fusion and predictive forecasting models.

*   **Deliverables:**
    *   Dual-band candidate fusion logic (FR-NOW-02).
    *   Integration of MLflow for model tracking.
    *   Forecasting Engine using XGBoost (FR-FORE-01, FR-FORE-03).
    *   Explainable AI (SHAP) integration (FR-XAI-01).
*   **Success Criteria:** The system correctly fuses dual-band data to reduce FAR and can generate a probability forecast for the next N minutes.

---

## 7. Phase 4: Serving, Experience & Polish (Sprint 4)

**Goal:** Build the user interfaces and prepare the platform for deployment and evaluation.

*   **Deliverables:**
    *   Dash dashboard for live visualization (FR-SRV-02).
    *   WebSocket integration for live alerts (FR-SRV-01, FR-SRV-03).
    *   Authentication and access control (FR-SEC-01).
    *   Comprehensive testing and documentation completion.
*   **Success Criteria:** A user can log into the dashboard, view historical light curves, and see live alerts populate via WebSocket when a flare is simulated.

---

## 8. Interfaces to Other Documents

- **`02_Software_Requirements_Specification.md`** — Defines the FRs referenced in each phase.
- **`09_Project_Timeline.md`** — Maps these phases to specific calendar dates.

---

## 9. Acceptance Criteria

- [ ] Clearly defines an MVP that represents a vertical slice of the architecture.
- [ ] Phases logically build upon each other (e.g., ingestion before processing before ML).

---

## 10. Review Checklist

- [ ] Does not contain hardcoded dates.
- [ ] Connects back to the vision outlined in `01_Project_Vision.md`.

---

## 11. Future Improvements

- Add a Phase 5 post-hackathon for multi-mission integration.

---

## Antigravity Development Prompt

```
PROJECT CONTEXT:
HeliosAI dual-band Aditya-L1 flare nowcasting/forecasting platform (ISRO PS-15).
Document 08 of 61: Development Roadmap.

FOLDER: docs/08_Development_Roadmap.md

FILES TO PRODUCE: docs/08_Development_Roadmap.md only.

CODING STANDARDS: Markdown. Follow the shared template.

EXPECTED OUTPUT: Phased roadmap defining Foundation, MVP, Advanced Intelligence, and
Serving/Polish.

EDGE CASES / VALIDATION: Ensure MVP represents a full vertical slice (ingestion through API),
not just horizontal layers.

TESTING: Markdown lint.

ACCEPTANCE CRITERIA: See §9 above.

DELIVERABLES: docs/08_Development_Roadmap.md

GIT COMMIT FORMAT: docs: add 08_Development_Roadmap.md (phased delivery plan)
```

---

**Next document:** `09_Project_Timeline.md` — say **NEXT** to continue.
