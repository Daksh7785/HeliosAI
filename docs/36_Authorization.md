# 36 — Authorization

> **Document 36 of 61** in the HeliosAI documentation set (see `README.md` → Repository Structure). Defines Role-Based Access Control (RBAC).

---

## Table of Contents

1. [Purpose of This Document](#purpose-of-this-document)
2. [Roles and Permissions](#roles-and-permissions)
3. [Implementation in FastAPI](#implementation-in-fastapi)

---

## Purpose of This Document

While Authentication (`35_Authentication.md`) verifies *who* the user is, Authorization verifies *what* they are allowed to do.

## Roles and Permissions

HeliosAI implements a simple RBAC system with three tiers:
1. **Viewer (Read-Only):** Can access the dashboard, view live light curves, and read the catalogue/forecasts. (Default role).
2. **Operator:** Can acknowledge alerts, trigger manual ingestion runs via the CLI or Admin Panel, and add notes to catalogue events.
3. **Admin:** Can manage users, modify system configuration thresholds, and access the underlying database directly.

## Implementation in FastAPI

Roles are embedded as claims within the JWT. FastAPI dependency injection (`Depends()`) is used to protect specific routes. For example, an endpoint to trigger manual ingestion requires `Depends(get_current_active_operator)`.

**Next document:** `37_Frontend_Architecture.md`
