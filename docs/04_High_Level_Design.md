# 04 — High-Level Design (HLD)

**HeliosAI** — AI-Powered Space Weather Intelligence Platform
Document 04 of 61

---

## 1. Purpose

This document translates the system architecture (`03_System_Architecture.md`) into software design patterns and boundaries. It explains how data moves between the logical blocks and the design choices governing those boundaries.

---

## 2. Core Design Patterns

### 2.1 The Pipeline Pattern (Data Flow)
The core of HeliosAI is an asynchronous Directed Acyclic Graph (DAG) for processing incoming telemetry.
- **Why:** Telemetry arrives out-of-band and needs sequential processing (parse -> sync -> feature engineer -> predict).
- **How:** Airflow orchestrates periodic ingestion; Celery handles the fine-grained, event-driven chain that processes individual time-chunks as they arrive.

### 2.2 The Strategy Pattern (ML Models)
The Forecasting Engine must support swapping out baseline XGBoost models for deep-sequence LSTM or Transformer models.
- **Why:** Allows continuous research and A/B testing of model families without changing the surrounding inference code.
- **How:** A unified `BaseModelPredictor` interface requires `predict()` and `explain()` methods, with concrete implementations wrapping scikit-learn or PyTorch models downloaded from the MLflow registry.

### 2.3 The Repository Pattern (Data Access)
Business logic (e.g., forecasting) must be decoupled from SQL queries.
- **Why:** Prevents tight coupling to TimescaleDB syntax and simplifies unit testing via mocked repositories.
- **How:** `src/shared/database/` contains classes (e.g., `FlareEventRepository`, `TelemetryRepository`) that handle all SQLAlchemy ORM operations.

### 2.4 Pub-Sub (Live Updates)
The dashboard needs real-time updates without aggressive database polling.
- **Why:** High-frequency polling on TimescaleDB degrades ingestion performance.
- **How:** When the Intelligence Layer inserts a new forecast into the database, it simultaneously publishes an event to a Redis channel. The FastAPI WebSocket manager subscribes to this channel and pushes the update to the connected Dash clients.

---

## 3. Subsystem Boundaries & Contracts

### 3.1 Ingestion <-> Processing
- **Contract:** Raw telemetry is written to the `raw_telemetry` table. A Celery task payload containing `(start_time, end_time)` is queued.
- **Isolation:** Processing does not know how to fetch from ISRO; it only knows how to read from the database window provided by the task.

### 3.2 Processing <-> Intelligence
- **Contract:** Engineered features are written to the `feature_store` table. A Celery task payload containing `(feature_snapshot_id)` is queued.
- **Isolation:** The Intelligence models assume clean, synced, `NaN`-free data. All interpolation logic is strictly encapsulated in the Processing layer.

### 3.3 Intelligence <-> Serving
- **Contract:** Predictions and SHAP values are written to `forecasts` and `explanations` tables. A Redis Pub/Sub message is broadcast with a summarized JSON payload.
- **Isolation:** The API never runs ML inference directly. It only queries the results from the database or passes through the Redis stream.

---

## 4. Error Handling & Resilience

- **Data Gaps:** Handled by the Processing layer. Small gaps are interpolated; large gaps trigger a "Quarantine" flag, preventing the Intelligence layer from making unreliable forecasts.
- **Component Failure:** If the MLflow registry is down, the Intelligence layer falls back to a locally cached model artifact. If Redis is down, WebSockets fail but REST API polling acts as a degraded fallback.

---

## 5. Interfaces to Other Documents

- **`05_Low_Level_Design.md`** — translates these patterns into specific Python classes and interfaces.
- **`30_Database_Design.md`** — defines the tables referenced in the boundaries section.

---

## 6. Acceptance Criteria

- [ ] Clear delineation of responsibilities between components (no "God objects").
- [ ] Explicit identification of the design patterns used (Pipeline, Strategy, Repository, Pub-Sub).
- [ ] Failure modes and degraded states are defined.

---

## 7. Review Checklist

- [ ] Does not contain specific SQL queries or Python code snippets (belongs in `05`).
- [ ] Consistent with the 5-layer architecture in `03`.

---

## 8. Future Improvements

- Map out an Event Sourcing pattern if the system requires full replayability of the data pipeline state over time.

---

## Antigravity Development Prompt

```
PROJECT CONTEXT:
You are implementing a documentation-only artifact — this task produces no source code.
Repository: HeliosAI. This is document 04 of a 61-document specification set.

FOLDER:
docs/04_High_Level_Design.md

FILES TO PRODUCE:
None (documentation task). Output exactly one file: docs/04_High_Level_Design.md

CODING STANDARDS:
N/A — Markdown only. Follow the structural template used by all other docs.

EXPECTED OUTPUT:
A single self-contained Markdown file outlining the HLD, patterns, and boundaries.

TESTING:
Documentation-only — validation is a Markdown lint pass.

ACCEPTANCE CRITERIA:
See §6 above.

DELIVERABLES:
docs/04_High_Level_Design.md

GIT COMMIT FORMAT:
docs: add 04_High_Level_Design.md (patterns and subsystem boundaries)
```

---

**Next document:** `05_Low_Level_Design.md` — say **NEXT** to continue.
