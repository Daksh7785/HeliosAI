# 41 — Admin Panel

**HeliosAI** — AI-Powered Space Weather Intelligence Platform
Document 41 of 61

---

## 1. Purpose

Specifies the administrative surface for HeliosAI, implemented in **Streamlit** (per `37_Frontend_Architecture.md`'s framework split) and restricted to the `admin` role (per `36_Authorization.md`).

---

## 2. Why Streamlit Here

The admin panel is a low-traffic, form-heavy, internally-facing tool. Streamlit's rapid form/table scaffolding is a better fit than hand-building equivalent Dash pages, keeping the primary Dash app focused on the high-traffic, real-time-critical dashboard.

---

## 3. Modules

| Module | Function |
|---|---|
| **User & Role Management** | Create/deactivate users, assign roles (`viewer`/`analyst`/`ml_engineer`/`admin`), issue/revoke service-account tokens |
| **Alert Threshold Configuration** | Adjust per-class confidence thresholds for nowcasting promotion and forecast trigger probability, with a preview of how the change would have affected recent historical data before saving |
| **Ingestion Status** | View Airflow DAG run history, last successful fetch per payload (SoLEXS/HEL1OS), manual re-trigger for failed fetches |
| **Model Registry Overview** | Read-only MLflow summary — current production model version per task (nowcasting-fusion, forecasting), promotion history |
| **System Health** | Surfaces key Prometheus/Grafana metrics (queue depth, ingestion latency, API error rate) without requiring admins to leave the app |
| **Data Retention & Export** | Configure raw-data retention windows (subject to TimescaleDB compression policy), trigger bulk catalogue exports |

---

## 4. Threshold Change Safety

Because alert thresholds directly affect the "High TPR / low FAR" evaluation criterion, threshold edits go through a two-step confirmation:

1. Admin adjusts a threshold slider; the panel immediately re-scores the last 30 days of historical candidates against the proposed threshold and shows a before/after precision-recall delta.
2. Admin confirms; the change is versioned (old value retained) and logged with actor identity per `44_Logging.md`.

---

## 5. Access & Isolation

- Served on a distinct route/subdomain from the primary dashboard, gated by the same JWT/role middleware described in `35_Authentication.md` / `36_Authorization.md`.
- No admin action bypasses the FastAPI backend — Streamlit forms call the same authenticated REST endpoints used elsewhere, so there is a single source of truth for business logic (no duplicated write paths).

---

## 6. Non-Goals

- The admin panel is not a general-purpose SQL console; direct database access is intentionally not exposed here to prevent unaudited writes.
- Model retraining is *triggered* here but *configured* (hyperparameters, data windows) in the MLOps tooling described in `46_MLOps.md`.

---

## 7. Interfaces to Other Documents

- **`37_Frontend_Architecture.md`** — hosting architecture for this Streamlit sub-app.
- **`36_Authorization.md`** — role gating for admin-only actions.
- **`46_MLOps.md`**, **`47_Model_Training.md`** — systems this panel surfaces status for.
- **`44_Logging.md`** — audit trail for admin actions.

---

**Next document:** `42_Alert_System.md` — say **NEXT** to continue.
