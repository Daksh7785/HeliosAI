# 44 — Logging

**HeliosAI** — AI-Powered Space Weather Intelligence Platform
Document 44 of 61

---

## 1. Purpose

Defines HeliosAI's logging strategy, supporting the Auditability non-functional requirement ("every catalogue entry and forecast must be traceable to a specific model version and data snapshot") and general operational debuggability across a multi-service pipeline.

---

## 2. Logging Stack

| Concern | Technology |
|---|---|
| Structured logging | `structlog`, wrapping Python's standard `logging` |
| Format | JSON lines (machine-parseable), human-readable console renderer for local dev |
| Aggregation (optional) | Loki, scraped alongside Prometheus metrics |
| Correlation | Request/trace ID propagated across FastAPI → Celery → Airflow task boundaries |

---

## 3. Log Levels & Usage

| Level | Usage |
|---|---|
| `DEBUG` | Verbose pipeline internals (feature values, intermediate model outputs) — enabled only in dev/staging |
| `INFO` | Normal operational events: ingestion completed, flare detected, alert dispatched, model retrained |
| `WARNING` | Recoverable anomalies: single-band-only detection, data gap filled by interpolation, retry succeeded |
| `ERROR` | Failed operation requiring attention: ingestion failure after retries, DB write failure |
| `CRITICAL` | Service-level failure impacting nowcasting/forecasting availability |

---

## 4. Required Structured Fields

Every log line includes, at minimum:

```json
{
  "timestamp": "2026-07-11T09:42:11.203Z",
  "level": "INFO",
  "service": "nowcasting-engine",
  "trace_id": "a1b2c3d4",
  "event": "flare_detected",
  "event_id": "evt_00123",
  "model_version": "nowcast-fusion-v2.3.1",
  "data_snapshot_id": "snap_2026-07-11T09",
  "message": "Flare candidate promoted to master catalogue"
}
```

The `model_version` and `data_snapshot_id` fields are mandatory on every nowcasting/forecasting decision log, directly satisfying the Auditability requirement.

---

## 5. Audit-Specific Logging

Distinct from operational logs, an **audit log** (append-only table in PostgreSQL, separate from application logs) records every state-changing action by an authenticated identity: logins, threshold changes, manual re-runs, retraining triggers, catalogue annotations. Audit log entries are never deleted, only retained per the configured compliance/retention policy.

---

## 6. Sensitive Data Handling

- No credentials, tokens, or raw secrets are ever logged, including in `DEBUG` mode (enforced via a `structlog` processor that redacts known sensitive field names).
- Personally identifying user data in logs is limited to user ID (not email/name) wherever practical, to minimize exposure surface.

---

## 7. Retention

| Log Type | Retention |
|---|---|
| Application/operational logs | 30 days (configurable), then discarded |
| Audit logs | Indefinite / per organizational policy |
| Model decision logs (nowcast/forecast triggers) | Indefinite — these double as the scientific record underlying the master catalogue |

---

## 8. Interfaces to Other Documents

- **`45_Monitoring.md`** — metrics derived from log streams (error rates, latency).
- **`36_Authorization.md`** — audit trail requirement this log design fulfills.
- **`54_Security.md`** — secret-redaction policy.
- **`30_Database_Design.md`** — audit log table schema.

---

**Next document:** `45_Monitoring.md` — say **NEXT** to continue.
