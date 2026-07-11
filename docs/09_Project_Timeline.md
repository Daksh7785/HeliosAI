# 09 — Project Timeline

**HeliosAI** — AI-Powered Space Weather Intelligence Platform
Document 09 of 61

---

## 1. Executive Summary

This document maps the phases defined in `08_Development_Roadmap.md` to an indicative timeline, structured around typical hackathon constraints (e.g., a 4-to-6-week sprint leading to final evaluation).

---

## 2. Purpose

Provide a shared understanding of scheduling constraints and critical path dependencies to ensure all required components for the final hackathon submission are delivered on time.

---

## 3. Scope

Covers the end-to-end development timeline.

---

## 4. Proposed Timeline (6-Week Model)

### 4.1 Week 1: Setup and Ingestion (Foundation)
- **Objective:** Establish the environment and ingest primary datasets.
- **Key Activities:**
  - Initialize repository and Docker environment.
  - Implement SoLEXS and HEL1OS download scripts (FR-ING-01).
  - Setup raw data database tables and initial migrations.
- **Milestone:** Data is flowing from ISRO PRADAN to the local `data/raw/` directory.

### 4.2 Week 2: Processing and Baseline (MVP)
- **Objective:** Build the core pipeline and a baseline detection model.
- **Key Activities:**
  - Implement time-synchronization (FR-PROC-01).
  - Extract baseline features (FR-PROC-03).
  - Create a simple rule-based nowcasting model (FR-NOW-01).
  - Scaffold FastAPI backend to serve results.
- **Milestone:** MVP completion. A basic pipeline runs end-to-end.

### 4.3 Week 3: Advanced Intelligence (Nowcasting)
- **Objective:** Implement dual-band fusion and robust nowcasting.
- **Key Activities:**
  - Implement fusion logic to reduce FAR (FR-NOW-02).
  - Integrate MLflow and start training models on historical flare events.
  - Setup model evaluation metrics logging (TPR, FAR).
- **Milestone:** Robust detection with quantifiable performance metrics.

### 4.4 Week 4: Advanced Intelligence (Forecasting & XAI)
- **Objective:** Develop predictive capabilities and explainability.
- **Key Activities:**
  - Train and evaluate XGBoost/LSTM forecasting models (FR-FORE-01).
  - Integrate SHAP for model explainability (FR-XAI-01).
  - Persist forecasts and explanations to the database.
- **Milestone:** Models can predict flares with a logged lead time and explain their reasoning.

### 4.5 Week 5: Serving and Experience
- **Objective:** Build out the user interface and real-time capabilities.
- **Key Activities:**
  - Finalize FastAPI REST endpoints (FR-SRV-01).
  - Implement WebSocket alerts.
  - Build the Dash dashboard for visualization (FR-SRV-02).
  - Implement RBAC (FR-SEC-02).
- **Milestone:** The system is fully usable via a web browser.

### 4.6 Week 6: Polish, Testing, and Submission
- **Objective:** Finalize the system for evaluation.
- **Key Activities:**
  - End-to-end testing and bug fixing.
  - Complete all documentation (`00` - `61`).
  - Finalize the `README.md` and submission materials.
  - Prepare the recorded demonstration.
- **Milestone:** Final Hackathon Submission.

---

## 5. Critical Path

The most critical path dependency is **Data Synchronization (Week 2)**. Without cleanly synchronized dual-band data, the advanced ML models (Weeks 3-4) cannot be effectively trained, which in turn blocks meaningful visualization (Week 5).

---

## 6. Interfaces to Other Documents

- **`08_Development_Roadmap.md`** — Defines the phases mapped to these weeks.

---

## 7. Acceptance Criteria

- [ ] Timeline maps directly to the phases in `08_Development_Roadmap.md`.
- [ ] Critical path dependencies are explicitly noted.

---

## 8. Review Checklist

- [ ] Ensure timeline is realistic for a small team over a 6-week period.

---

## 9. Future Improvements

- Update timeline with actual completion dates retrospectively.

---

## Antigravity Development Prompt

```
PROJECT CONTEXT:
HeliosAI dual-band Aditya-L1 flare nowcasting/forecasting platform (ISRO PS-15).
Document 09 of 61: Project Timeline.

FOLDER: docs/09_Project_Timeline.md

FILES TO PRODUCE: docs/09_Project_Timeline.md only.

CODING STANDARDS: Markdown. Follow the shared template.

EXPECTED OUTPUT: A 6-week indicative timeline mapping activities and milestones.

EDGE CASES / VALIDATION: None.

TESTING: Markdown lint.

ACCEPTANCE CRITERIA: See §7 above.

DELIVERABLES: docs/09_Project_Timeline.md

GIT COMMIT FORMAT: docs: add 09_Project_Timeline.md (6-week schedule)
```

---

**Next document:** `10_Risk_Assessment.md` — say **NEXT** to continue.
