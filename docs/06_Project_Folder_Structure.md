# 06 — Project Folder Structure

**HeliosAI** — AI-Powered Space Weather Intelligence Platform
Document 06 of 61

---

## 1. Purpose

This document defines the canonical directory structure of the HeliosAI repository. It ensures that all engineers, models, and scripts expect code, data, and configurations to exist in predictable locations, maintaining alignment with the Modular Monolith architecture described in `03_System_Architecture.md`.

---

## 2. Root Directory Structure

The repository is organized into top-level directories separating application code, infrastructure, documentation, and data.

```text
HeliosAI/
├── .github/                # CI/CD workflows and GitHub templates
├── data/                   # Local data storage (git-ignored)
├── deploy/                 # Deployment scripts and compose files
├── docs/                   # Full documentation suite (00-61)
├── infra/                  # Infrastructure as Code (Terraform/K8s)
├── models/                 # Serialized model artifacts (git-ignored)
├── notebooks/              # Jupyter notebooks for EDA and research
├── pipeline/               # Airflow DAGs
├── prompts/                # Antigravity master prompts for AI assistance
├── scripts/                # Utility and administration scripts
├── src/                    # Primary application source code
├── tests/                  # Test suites and fixtures
├── .env.example            # Environment variable template
├── app.py                  # API Entrypoint
├── docker-compose.yml      # Base docker-compose configuration
├── Dockerfile              # Multi-stage Docker build
├── Makefile                # Task runner shortcuts
├── pyproject.toml          # Python dependencies and tool configs
└── README.md               # Repository entry point
```

---

## 3. `src/` Directory Breakdown

The `src/` directory houses the core application, strictly adhering to domain boundaries.

```text
src/
├── ingestion/              # Subsystem: Data Fetching & Parsing
│   ├── solexs/             # SoLEXS specific fetchers/parsers
│   └── hel1os/             # HEL1OS specific fetchers/parsers
├── processing/             # Subsystem: Syncing & Feature Engineering
│   ├── time_sync.py        # Resampling and alignment logic
│   └── feature_gen.py      # Hardness ratio, wavelet transforms
├── intelligence/           # Subsystem: ML Models & Inference
│   ├── nowcast/            # Active flare detection logic
│   ├── forecast/           # Future probability models
│   └── xai/                # Explainability (SHAP) generators
├── serving/                # Subsystem: API & WebSockets
│   ├── api/                # FastAPI routes and controllers
│   ├── ws/                 # WebSocket connection managers
│   └── background/         # Celery task definitions
├── frontend/               # Subsystem: Dash & Streamlit UI
│   ├── components/         # Reusable UI widgets
│   ├── pages/              # Dashboard layouts
│   └── callbacks/          # Dash interactivity logic
└── shared/                 # Cross-cutting concerns
    ├── database/           # SQLAlchemy models and Repositories
    ├── config/             # Pydantic settings management
    └── logging.py          # Structured logging setup
```

---

## 4. `tests/` Directory Breakdown

Tests mirror the `src/` directory structure but are separated by test type.

```text
tests/
├── unit/                   # Fast, isolated tests without DB access
│   ├── test_ingestion/
│   ├── test_processing/
│   └── ...
├── integration/            # Slower tests requiring DB/Redis
│   ├── test_api_flow.py
│   └── test_celery_tasks.py
├── e2e/                    # End-to-End pipeline tests
│   └── test_full_pipeline.py
├── fixtures/               # Test data (e.g., sample FITS files)
└── conftest.py             # Shared pytest fixtures
```

---

## 5. `data/` Directory (Git-Ignored)

Local execution requires a standardized location for transient or raw data files. This directory is strictly ignored by Git to prevent committing large binaries or sensitive info.

```text
data/
├── raw/                    # Downloaded FITS files from ISRO
├── processed/              # Intermediate data dumps
└── cache/                  # Redis/job temporary storage
```

---

## 6. Interfaces to Other Documents

- **`03_System_Architecture.md`** — provides the logical mapping for the physical `src/` directories.
- **`56_Coding_Standards.md`** — defines the import rules across these directories (e.g., avoiding circular dependencies between subsystems).

---

## 7. Acceptance Criteria

- [ ] Directory structure strictly prevents cyclical imports between top-level `src/` subsystems.
- [ ] The `shared/` folder contains only cross-cutting utilities (DB, config, logging) and no domain-specific business logic.
- [ ] Every subsystem defined in `03` has a corresponding directory in `src/`.

---

## 8. Review Checklist

- [ ] `data/` and `models/` must be included in `.gitignore`.
- [ ] No frontend code (Dash/Streamlit) should reside outside of `src/frontend/`.

---

## 9. Future Improvements

- If the application transitions to a true microservices architecture, the `src/` subdirectories may be split into entirely independent repositories or top-level project folders.

---

## Antigravity Development Prompt

```
PROJECT CONTEXT:
You are implementing a documentation-only artifact — this task produces no source code.
Repository: HeliosAI. This is document 06 of a 61-document specification set.

FOLDER:
docs/06_Project_Folder_Structure.md

FILES TO PRODUCE:
None (documentation task). Output exactly one file: docs/06_Project_Folder_Structure.md

CODING STANDARDS:
N/A — Markdown only. Follow the structural template used by all other docs.

EXPECTED OUTPUT:
A single self-contained Markdown file outlining the directory tree and rules.

TESTING:
Documentation-only — validation is a Markdown lint pass.

ACCEPTANCE CRITERIA:
See §7 above.

DELIVERABLES:
docs/06_Project_Folder_Structure.md

GIT COMMIT FORMAT:
docs: add 06_Project_Folder_Structure.md (directory layout)
```

---

**Next document:** `07_Tech_Stack.md` — say **NEXT** to continue.
