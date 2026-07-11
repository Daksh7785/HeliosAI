# 31 — Backend Architecture

> **Document 31 of 61** in the HeliosAI documentation set (see `README.md` → Repository Structure). Defines the Serving Layer's macro-architecture.

---

## Table of Contents

1. [Purpose of This Document](#purpose-of-this-document)
2. [Serving Layer Responsibilities](#serving-layer-responsibilities)
3. [Technology Stack](#technology-stack)
4. [Service Interactions](#service-interactions)
5. [Concurrency and Scaling](#concurrency-and-scaling)

---

## Purpose of This Document

This document defines the `services/api/` module. It bridges the gap between the intelligence engines (Nowcasting and Forecasting) and the human-facing Experience Layer (Dashboard and CLI).

## Serving Layer Responsibilities

The Backend Architecture is responsible for:
- Providing secure, versioned REST endpoints (`32_API_Design.md`).
- Broadcasting real-time telemetry and flare alerts to connected clients (`33_WebSocket_System.md`).
- Managing user authentication and role-based access (`35_Authentication.md`, `36_Authorization.md`).

## Technology Stack

- **Framework:** FastAPI (Python). Chosen for native async support, automated OpenAPI documentation generation, and high performance.
- **ASGI Server:** Uvicorn, running behind Gunicorn workers for production stability.
- **ORM:** SQLAlchemy 2.0 (asyncio mode) interacting with TimescaleDB.

## Service Interactions

The API is strictly a **consumer** of data. It does not run inference or ingestion tasks directly.
- It queries the database populated by `services/intelligence/`.
- If an on-demand task is requested (e.g., a manual data ingestion run triggered via CLI), the API dispatches a message to the Celery broker, which is picked up by `services/ingestion/` or `services/processing/`.

## Concurrency and Scaling

Because FastAPI natively supports asynchronous I/O (`async def`), the backend can handle thousands of concurrent WebSocket connections and slow database queries without blocking the main event loop. Horizontal scaling is achieved via Kubernetes deployments (`51_Kubernetes.md`) replicating the API pods behind a LoadBalancer.

**Next document:** `32_API_Design.md`
