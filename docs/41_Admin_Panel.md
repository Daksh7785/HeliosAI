# 41 — Admin Panel

> **Document 41 of 61** in the HeliosAI documentation set (see `README.md` → Repository Structure). Defines the management interface for the system.

---

## Table of Contents

1. [Purpose of This Document](#purpose-of-this-document)
2. [Target Audience](#target-audience)
3. [Core Capabilities](#core-capabilities)
4. [Security](#security)

---

## Purpose of This Document

The Admin Panel is a restricted sub-route of the Dashboard (`/admin`) designed to manage the operational state of HeliosAI without requiring CLI access.

## Target Audience

Operators and Admins (defined in `36_Authorization.md`).

## Core Capabilities

- **User Management:** Create/revoke accounts and change RBAC roles.
- **Threshold Tuning:** A form interface to hot-reload the threshold values (e.g., CUSUM drift parameters, background subtraction windows) stored in the database without restarting the backend.
- **Manual Ingestion Trigger:** A file-upload component to drop L1 data files directly into the quarantine/processing queue if the automated fetcher fails.
- **System Health:** A summarized view of Celery queue lengths and database connection statuses.

## Security

This route is strictly guarded by the `Admin` role claim in the JWT. The API (`services/api/rest_routes_admin/`) will reject any request lacking this claim with a `403 Forbidden`.

**Next document:** `42_Alert_Dispatcher.md`
