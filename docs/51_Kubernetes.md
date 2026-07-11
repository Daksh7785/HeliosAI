# 51 — Kubernetes Architecture

> **Document 51 of 61** in the HeliosAI documentation set (see `README.md` → Repository Structure). Defines the container orchestration layer.

---

## Table of Contents

1. [Purpose of This Document](#purpose-of-this-document)
2. [Cluster Topology](#cluster-topology)
3. [Autoscaling Strategy](#autoscaling-strategy)
4. [Ingress and Routing](#ingress-and-routing)

---

## Purpose of This Document

Once Terraform (`50_Infrastructure.md`) provisions the underlying virtual machines, Kubernetes handles deploying, scaling, and healing the HeliosAI microservices.

## Cluster Topology

The system is deployed across multiple Namespaces:
- `helios-core`: The FastAPI backend, Celery workers, and the Intelligence Subsystem consumers.
- `helios-data`: Airflow scheduler and workers for batch ingestion.
- `helios-mlops`: The MLflow Tracking Server.
- `helios-frontend`: The Dash application.

## Autoscaling Strategy

- **Horizontal Pod Autoscaler (HPA):** Scales the `services/api/` and `services/dashboard/` deployments based on CPU/Memory usage (e.g., during a major solar storm when traffic spikes).
- **KEDA (Kubernetes Event-driven Autoscaling):** Scales the Celery worker pods based on the length of the Redis task queues, ensuring heavy processing tasks (like Explainability generation) don't bottleneck.

## Ingress and Routing

An NGINX Ingress Controller routes external traffic:
- `api.heliosai.org` -> `services/api/`
- `dashboard.heliosai.org` -> `services/dashboard/`
- `mlflow.internal.heliosai.org` -> MLflow Server (VPN restricted).

**Next document:** `52_CI_CD.md`
