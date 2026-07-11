# 51 — Kubernetes

**HeliosAI** — AI-Powered Space Weather Intelligence Platform
Document 51 of 61

---

## 1. Purpose

Describes the **optional** scale-out deployment path for HeliosAI, for organizations moving beyond a single-host Docker Compose deployment (e.g., multi-org hosting, higher availability, larger ingestion/training workloads).

---

## 2. When Kubernetes Is Warranted

Per the README's Orchestration row ("optional, scale-out"), Kubernetes is **not** the default deployment path — Docker Compose remains the primary, documented quickstart. Kubernetes is recommended when:
- Multiple research organizations are hosted on shared infrastructure (namespace isolation).
- Celery worker/Airflow DAG concurrency needs exceed single-host capacity.
- High-availability requirements emerge beyond the research/decision-support scope noted in the README's Out of Scope section.

---

## 3. Manifest Structure

```
infra/k8s/
├── namespace.yaml
├── configmaps/
├── secrets/                # sealed-secrets or external-secrets references, never plaintext
├── deployments/
│   ├── api.yaml
│   ├── dash.yaml
│   ├── streamlit.yaml
│   ├── celery-worker.yaml
│   └── mlflow.yaml
├── statefulsets/
│   ├── postgres-timescaledb.yaml
│   └── redis.yaml
├── services/
├── ingress.yaml
└── hpa/                     # HorizontalPodAutoscaler definitions
```

---

## 4. Scaling Policy

| Component | Scaling Approach |
|---|---|
| `api` (FastAPI) | HPA on CPU + request-latency custom metric |
| `celery-worker` | HPA on Redis queue-depth custom metric (KEDA-based, scales toward zero during quiet-Sun periods) |
| `dash` / `streamlit` | HPA on CPU/connection count |
| `postgres-timescaledb` | StatefulSet, vertical scaling preferred over horizontal for the primary; read replicas optional for analytics load (`43_Analytics.md`) |

---

## 5. Reliability Patterns

- Liveness/readiness probes map directly to the `/healthz` / `/readyz` endpoints defined in `45_Monitoring.md`.
- `PodDisruptionBudget`s on `api` and `dash` prevent simultaneous eviction of all replicas during node maintenance.
- Rolling update strategy (`maxUnavailable: 0`) ensures the nowcasting alert path is never fully offline during a deploy.

---

## 6. Secrets on Kubernetes

Secrets are managed via `external-secrets` (syncing from Vault/cloud secrets manager) or `sealed-secrets`, never as plaintext `Secret` manifests committed to the repository — consistent with `54_Security.md`.

---

## 7. Relationship to Docker Compose Path

The same container images built for Docker Compose (`50_Docker.md`) are reused unchanged for Kubernetes manifests — Kubernetes is a deployment-orchestration choice, not a separate build target, keeping the two paths from diverging.

---

## 8. Interfaces to Other Documents

- **`49_Deployment.md`**, **`50_Docker.md`** — the deployment/image foundation this extends.
- **`45_Monitoring.md`** — health probe contracts.
- **`54_Security.md`** — secrets and network policy.

---

**Next document:** `52_CI_CD.md` — say **NEXT** to continue.
