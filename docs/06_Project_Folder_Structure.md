# 06 — Project Folder Structure

**HeliosAI** — AI-Powered Space Weather Intelligence Platform
Document 06 of 61

---

## 1. Purpose

This document outlines the standard directory structure for the HeliosAI repository, providing a high-level map of where code, configuration, documentation, and tests reside. It ensures consistency across the project and helps developers navigate the codebase efficiently.

---

## 2. Root Directory Structure

The repository is organized following standard Python/FastAPI and modern frontend practices.

```text
HeliosAI/
├── .github/                  # GitHub Actions workflows (CI/CD)
├── docs/                     # Comprehensive project documentation (numbered series)
├── src/                      # Main application source code
│   ├── frontend/             # Dash/React UI layer
│   ├── serving/              # FastAPI backend API
│   ├── pipeline/             # Data ingestion and processing pipelines
│   ├── shared/               # Shared utilities, database models, and common logic
│   ├── flare_detector.py     # Nowcasting algorithm core
│   ├── forecaster.py         # ML Forecasting logic (XGBoost)
│   └── data_loader.py        # Telemetry ingestion/simulation
├── tests/                    # Automated test suite (pytest)
│   ├── unit/                 # Fast, isolated tests
│   └── integration/          # Tests requiring DB or multiple components
├── data/                     # Local data storage for dev (simulated telemetry, etc.)
├── models/                   # Saved ML models (e.g., .pkl files)
├── docker-compose.yml        # Development environment services
├── docker-compose.dev.yml    # Overrides for local development
├── requirements.txt          # Python dependencies
├── README.md                 # Project overview and quickstart
└── MASTER_DOCUMENTATION_PLAN.md # Blueprint for all docs
```

---

## 3. Key Subsystem Details

### 3.1 `src/serving/` (API Layer)
Handles external HTTP requests and serves data to the frontend and third-party consumers.
*   **`api/main.py`**: The FastAPI application entry point, defining routes and dependency injections.
*   **`api/routers/`**: Grouped API endpoints (e.g., telemetry, catalogue).

### 3.2 `src/shared/` (Common Core)
Contains code used across multiple subsystems (API, Pipeline, CLI).
*   **`database/db.py`**: SQLAlchemy engine and session management.
*   **`database/models.py`**: ORM definitions mapping to database tables (`FeatureStore`, `FlareCatalogue`).

### 3.3 `src/pipeline/` (Data Processing)
Houses the background jobs and stream processing logic.
*   **`realtime_simulator.py`**: Simulates live telemetry feed and runs real-time nowcasting/forecasting.
*   (Future) **`ingestion/`**: Scripts for fetching live ISRO data when available.

### 3.4 `src/frontend/` (User Experience)
The web-based dashboard for human-in-the-loop monitoring.
*   **`app.py`**: The main Plotly Dash application.
*   **`pages/`**: (Future) Additional dashboard views (e.g., Admin Panel, Historical Analysis).

---

## 4. Environment-Specific Overrides

*   **Local Development**: Relies on `requirements.txt` for dependencies and local SQLite (`heliosai.db`) or Docker Compose for services.
*   **Production**: Relies on Docker images built via CI/CD, connected to managed cloud databases (PostgreSQL, Redis) and orchestrated via Kubernetes.

---

## 5. Documentation Mapping

All documentation lives in `docs/` and follows a strict two-digit numbering scheme (00-61) defined in `MASTER_DOCUMENTATION_PLAN.md`.

*   `00`-`05`: Core architecture and specs.
*   `06`-`15`: Development environment and structure.
*   `22`-`29`: Algorithms and Machine Learning.
*   `30`-`42`: Subsystem designs.

---
*End of Document 06*
