# 54 — Security

**HeliosAI** — AI-Powered Space Weather Intelligence Platform
Document 54 of 61

---

## 1. Purpose

Consolidates HeliosAI's security posture across authentication, authorization, secrets, network, and dependency management, directly implementing the README's Security non-functional requirement.

---

## 2. Threat Model Summary

| Asset | Primary Threats | Mitigation |
|---|---|---|
| User credentials / JWTs | Credential stuffing, token theft | Argon2id hashing, short-lived access tokens, HTTP-only cookies (`35_Authentication.md`) |
| Master flare catalogue / scientific data | Unauthorized modification, data poisoning affecting model retraining | RBAC write restrictions (`36_Authorization.md`), audit logging (`44_Logging.md`) |
| Model artifacts | Supply-chain tampering, unauthorized promotion to Production | MLflow registry access control, promotion gate (`46_MLOps.md`, `48_Model_Evaluation.md`) |
| API/WebSocket endpoints | DoS, injection, unauthorized access | Rate limiting, input validation (Pydantic), auth middleware on every route |
| Secrets (DB creds, signing keys) | Leakage via code/logs/images | No hardcoded secrets, Vault/external-secrets, log redaction (`44_Logging.md`) |
| Container images | Known-CVE dependencies, oversized attack surface | Multi-stage minimal images, `pip-audit`/`bandit` in CI (`52_CI_CD.md`) |

---

## 3. Transport Security

- TLS termination at NGINX (`50_Docker.md`), HTTP→HTTPS redirect enforced.
- Internal service-to-service traffic confined to a private Docker/Kubernetes network, not exposed to the host network beyond the reverse proxy.

---

## 4. Application-Level Protections

| Protection | Mechanism |
|---|---|
| Input validation | Pydantic models on every FastAPI request/response boundary |
| SQL injection | SQLAlchemy ORM with parameterized queries exclusively — no raw string-interpolated SQL |
| Rate limiting | Redis-backed sliding-window limiter on auth and public API endpoints |
| CSRF | Not applicable to token-bearer API calls; Dash session cookie uses `SameSite=Strict` |
| Dependency vulnerabilities | `pip-audit` in CI, scheduled weekly re-scan even without new commits |
| Webhook payload integrity | HMAC-signed outbound webhook payloads (`42_Alert_System.md`) |

---

## 5. Secrets Rotation Policy

| Secret | Rotation Cadence |
|---|---|
| JWT signing keys | Documented rotation schedule, dual-key grace window (`35_Authentication.md`) |
| Service-account tokens | 24-hour lifetime, auto-rotated |
| Database credentials | Rotated per organizational policy, never embedded in images |
| Webhook signing secrets | Rotated on demand via Admin Panel, old secret honored for a grace period |

---

## 6. Access Review

Periodic (documented cadence, tracked outside this static document to avoid staleness) review of active user accounts, roles, and service-account tokens by an `admin`, cross-referenced against the audit log (`44_Logging.md`) for unused/stale grants.

---

## 7. Incident Response Notes

- Security-relevant log events (repeated auth failures, unusual admin actions) feed the same Monitoring/Alerting path as operational metrics (`45_Monitoring.md`), routed to `admin`.
- Given HeliosAI's explicit Out-of-Scope status as a non-certified, non-safety-of-life system, incident response is scoped to data integrity and service availability, not physical/mission-safety response protocols.

---

## 8. Interfaces to Other Documents

- **`35_Authentication.md`**, **`36_Authorization.md`** — identity/access controls this document consolidates.
- **`44_Logging.md`** — audit and security event logging.
- **`50_Docker.md`**, **`51_Kubernetes.md`** — image and network hardening.
- **`52_CI_CD.md`** — automated scanning gates.

---

**Next document:** `55_Performance_Optimization.md` — say **NEXT** to continue.
