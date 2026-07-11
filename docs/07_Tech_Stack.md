# 07 — Tech Stack

**HeliosAI** — AI-Powered Space Weather Intelligence Platform
Document 07 of 61

---

## 1. Executive Summary

This document enumerates the languages, frameworks, and core libraries used to build HeliosAI. It provides the specific "what" (e.g., FastAPI, TimescaleDB) to the architectural "why" defined in `03_System_Architecture.md`.

---

## 2. Purpose

Establish a rigid technology boundary to prevent tool sprawl. Every new dependency introduced during implementation must be justified against this list.

---

## 3. Scope

Covers backend, frontend, ML, database, and infrastructure choices.

---

## 4. Core Language

- **Python 3.12+**: The entire stack (frontend, backend, ML) is strictly Python-based to maximize accessibility for the heliophysics research community. No JavaScript/TypeScript, Go, or Rust services are permitted in the core monorepo.

---

## 5. Subsystem Tech Stacks

### 5.1 Ingestion & Processing
- **Apache Airflow**: Orchestrates the daily/hourly scheduled ingest of bulk ISRO files.
- **Celery (with Redis broker)**: Handles fine-grained, real-time processing chunks as telemetry arrives out-of-band.
- **Pandas / NumPy**: Core data structures for time-series manipulation.
- **Astropy / SunPy**: Standard heliophysics libraries for FITS file handling and solar coordinate transformations.

### 5.2 Intelligence (ML/DL)
- **Scikit-Learn**: Baseline models and preprocessing.
- **XGBoost**: Primary gradient-boosted tree model for structured feature forecasting.
- **PyTorch**: Deep learning backend for sequence models (LSTM/Transformers).
- **SHAP (SHapley Additive exPlanations)**: Core explainability library.

### 5.3 Data & Catalogue
- **PostgreSQL 16+**: Relational metadata and catalogue storage.
- **TimescaleDB**: PostgreSQL extension optimized for high-ingest time-series telemetry.
- **Redis**: In-memory caching and Pub/Sub message brokering.
- **MLflow**: Model registry, experiment tracking, and artifact storage.
- **SQLAlchemy (Async)**: ORM for database interaction.
- **Alembic**: Database migration management.

### 5.4 Serving (API)
- **FastAPI**: High-performance async REST framework.
- **Uvicorn / Gunicorn**: ASGI server and process manager.
- **Pydantic**: Data validation and serialization.
- **Starlette WebSockets**: Live data streaming.

### 5.5 Experience (Frontend)
- **Plotly Dash**: Main dashboard for live, interactive time-series visualizations.
- **Streamlit**: Internal admin panel and rapid-prototyping interface.

### 5.6 Infrastructure & DevOps
- **Docker & Docker Compose**: Containerization and local orchestration.
- **Kubernetes (Helm)**: Production scale-out orchestration (optional).
- **Terraform**: Infrastructure-as-Code for cloud deployments.
- **GitHub Actions**: CI/CD pipelines (linting, testing, image building).
- **Pytest**: Unit and integration testing framework.
- **Ruff / Black**: Code formatting and linting.

---

## 6. Architecture Mapping

| Subsystem (from `03_System_Architecture.md`) | Primary Technologies |
|---|---|
| Ingestion | Airflow, Astropy, SunPy |
| Processing | Celery, Pandas, NumPy |
| Intelligence | XGBoost, PyTorch, SHAP |
| Data & Catalogue | TimescaleDB, MLflow, Redis |
| Serving | FastAPI, SQLAlchemy |
| Experience | Dash, Plotly, Streamlit |

---

## 7. Acceptance Criteria

- [ ] All technologies align with the "100% Python" and "Open Source" guiding principles.
- [ ] Subsystem mapping covers all six architectural subsystems.

---

## 8. Review Checklist

- [ ] No proprietary SaaS lock-in (e.g., AWS specific services) mandated at the code level.
- [ ] Tech stack versions are reasonably modern (Python 3.12, Postgres 16).

---

## 9. Future Improvements

- Re-evaluate Polars as a replacement for Pandas if ingestion bottlenecks occur at scale.

---

## Antigravity Development Prompt

```
PROJECT CONTEXT:
HeliosAI dual-band Aditya-L1 flare nowcasting/forecasting platform (ISRO PS-15).
Document 07 of 61: Tech Stack.

FOLDER: docs/07_Tech_Stack.md

FILES TO PRODUCE: docs/07_Tech_Stack.md only.

CODING STANDARDS: Markdown. Follow the shared template. Ensure strict adherence to the
Python-only mandate.

EXPECTED OUTPUT: Enumeration of technologies broken down by subsystem, aligning with the
architecture document.

EDGE CASES / VALIDATION: Do not include React, Node.js, or other non-Python frontend
frameworks.

TESTING: Markdown lint.

ACCEPTANCE CRITERIA: See §7 above.

DELIVERABLES: docs/07_Tech_Stack.md

GIT COMMIT FORMAT: docs: add 07_Tech_Stack.md (technology selection)
```

---

**Next document:** `08_Development_Roadmap.md` — say **NEXT** to continue.
