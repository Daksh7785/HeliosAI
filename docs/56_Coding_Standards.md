# 56 — Coding Standards

**HeliosAI** — AI-Powered Space Weather Intelligence Platform
Document 56 of 61

---

## 1. Purpose

Establishes consistent code style and structural conventions across HeliosAI's all-Python codebase, so contributors (human or Antigravity-assisted AI) produce interoperable, reviewable code.

---

## 2. Language & Tooling

| Concern | Standard |
|---|---|
| Python version | 3.12+ |
| Formatting | `black` (enforced, not merely suggested) |
| Import ordering | `isort`, `black`-compatible profile |
| Linting | `ruff` (replaces flake8/pylint for speed) |
| Type checking | `mypy`, strict mode on `src/backend/` and `src/processing/`; relaxed on exploratory `notebooks/` |
| Docstrings | Google-style docstrings on all public functions/classes |

---

## 3. Project Layout Conventions

- One module = one responsibility; avoid "god modules" mixing ingestion, processing, and modeling concerns (each has its own package under `src/`, per `06_Project_Folder_Structure.md`).
- Shared Pydantic schemas (API contracts, feature records) live in a single `src/schemas/` package, imported everywhere rather than redefined per-module, keeping `32_API_Design.md` contracts single-sourced.

---

## 4. Naming Conventions

| Element | Convention |
|---|---|
| Modules/packages | `snake_case` |
| Classes | `PascalCase` |
| Functions/variables | `snake_case` |
| Constants | `UPPER_SNAKE_CASE` |
| Pydantic models | `PascalCase`, suffixed by role (`FlareEventIn`, `FlareEventOut`) |

---

## 5. Function & Module Design Principles

- Pure functions preferred for signal-processing and feature-engineering code (`20_Signal_Processing.md`, `21_Feature_Engineering.md`) — easier to unit test and to run under Hypothesis property-based tests (`53_Testing.md`).
- Side-effecting code (DB writes, external API calls) isolated at clearly named boundaries (`*_repository.py`, `*_client.py`), never mixed into scientific computation modules.
- No bare `except:` clauses; exceptions are caught narrowly and re-raised with context where appropriate, feeding structured logs (`44_Logging.md`).

---

## 6. ML Code Conventions

- Training scripts are deterministic given a fixed seed (seed always logged to MLflow, per `47_Model_Training.md`).
- Model classes implement a shared internal interface (`fit`, `predict`, `predict_proba`, `explain`) so nowcasting/forecasting engines can swap model families without call-site changes.

---

## 7. Commit-Level Expectations

- Every PR passes `black`, `ruff`, `mypy`, and the relevant test suite locally before push (mirrored by CI, `52_CI_CD.md`).
- Commit messages follow Conventional Commits (`feat:`, `fix:`, `docs:`, `refactor:`, `test:`), enabling automated changelog generation.

---

## 8. Documentation-in-Code

- Every module touching a scientific concept (flare classification, hardness ratio, lead time) includes a short docstring-level explanation of the domain concept, not just the code mechanics — bridging the gap between this documentation set and the implementation for future contributors.

---

## 9. Interfaces to Other Documents

- **`06_Project_Folder_Structure.md`** — the layout these standards assume.
- **`53_Testing.md`** — test conventions complementing these code standards.
- **`57_Git_Workflow.md`** — commit/branch conventions.
- **`61_Antigravity_Master_Prompt.md`** — how these standards are enforced in AI-assisted module implementation.

---

**Next document:** `57_Git_Workflow.md` — say **NEXT** to continue.
