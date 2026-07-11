# 50 — Docker

**HeliosAI** — AI-Powered Space Weather Intelligence Platform
Document 50 of 61

---

## 1. Purpose

Specifies container-level packaging details underpinning `49_Deployment.md`, covering per-service Dockerfiles and the `docker-compose.yml` contract.

---

## 2. Container Inventory

| Service | Base Image | Notes |
|---|---|---|
| `api` (FastAPI) | `python:3.12-slim` | Multi-stage build; Uvicorn workers behind Gunicorn in production mode |
| `dash` | `python:3.12-slim` | Serves Plotly Dash app |
| `streamlit` | `python:3.12-slim` | Admin panel |
| `celery-worker` | Same image as `api` (shared codebase, different entrypoint) | Scales horizontally by replica count |
| `airflow-scheduler` / `airflow-webserver` | Official `apache/airflow` image, extended with project DAGs | |
| `postgres` | `timescale/timescaledb-ha` (PostgreSQL + TimescaleDB extension) | |
| `redis` | Official `redis:alpine` | |
| `mlflow` | Custom image (`python:3.12-slim` + `mlflow` package) | |
| `nginx` | Official `nginx:alpine` | Reverse proxy / TLS termination |

---

## 3. Multi-Stage Build Pattern (api / celery-worker)

```dockerfile
# Stage 1: build dependencies
FROM python:3.12-slim AS builder
WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN pip install poetry && poetry export -f requirements.txt --output requirements.txt
RUN pip install --prefix=/install -r requirements.txt

# Stage 2: runtime
FROM python:3.12-slim
WORKDIR /app
COPY --from=builder /install /usr/local
COPY src/ ./src/
USER appuser
HEALTHCHECK CMD curl -f http://localhost:8000/healthz || exit 1
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Multi-stage builds keep runtime images free of build toolchains, reducing image size and attack surface (relevant to `54_Security.md`).

---

## 4. `docker-compose.yml` Conventions

- Named volumes for `postgres_data`, `redis_data`, `mlflow_artifacts` — ensuring data survives container recreation.
- All services declare `healthcheck` blocks, consumed by `depends_on: condition: service_healthy` so, e.g., `api` never starts accepting traffic before `postgres` is actually ready.
- Environment variables sourced from `.env`, never hardcoded into the compose file.
- A dedicated internal Docker network isolates inter-service traffic; only `nginx` exposes host ports.

---

## 5. Image Tagging & Registry

Images are tagged `heliosai/<service>:<git-short-sha>` and `heliosai/<service>:latest` (latest only for non-production convenience), pushed to the project's container registry by the CI/CD pipeline (`52_CI_CD.md`) on merge to the main branch.

---

## 6. Local Developer Experience

- `docker compose -f docker-compose.dev.yml up` mounts source directories as volumes for hot-reload (Uvicorn `--reload`, Dash debug mode).
- A separate `docker-compose.dev.yml` overlay keeps production and development configurations from diverging silently.

---

## 7. Interfaces to Other Documents

- **`49_Deployment.md`** — deployment flow consuming these containers.
- **`51_Kubernetes.md`** — Kubernetes manifests built from these same images.
- **`52_CI_CD.md`** — build/push automation.
- **`54_Security.md`** — image-hardening and scanning policy.

---

**Next document:** `51_Kubernetes.md` — say **NEXT** to continue.
