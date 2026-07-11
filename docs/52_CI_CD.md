# 52 — CI/CD Pipelines

> **Document 52 of 61** in the HeliosAI documentation set (see `README.md` → Repository Structure). Defines how code moves from GitHub to Kubernetes.

---

## Table of Contents

1. [Purpose of This Document](#purpose-of-this-document)
2. [Continuous Integration (CI)](#continuous-integration-ci)
3. [Continuous Deployment (CD)](#continuous-deployment-cd)
4. [Release Strategy](#release-strategy)

---

## Purpose of This Document

This document outlines the GitHub Actions workflows that automate testing and deployment, ensuring human error does not bring down the forecasting engine.

## Continuous Integration (CI)

Triggered on every PR to `main`:
1. **Linting:** Flake8 and Black verify Python formatting.
2. **Type Checking:** Mypy ensures type hints are correct.
3. **Unit Tests:** Pytest runs the suite in `tests/` (`58_Unit_Testing.md`), mocking external dependencies (PRADAN, Redis).
4. **Security Scan:** Bandit checks for hardcoded secrets or known vulnerabilities.

## Continuous Deployment (CD)

Triggered when a PR is merged to `main`:
1. **Docker Build:** `docker build` runs for each updated service (`api`, `dashboard`, `intelligence`).
2. **Push:** Images are tagged with the Git SHA and pushed to the container registry (e.g., ECR).
3. **Deploy:** `kubectl apply` updates the Kubernetes deployments (`51_Kubernetes.md`) with the new image tags via a rolling update.

## Release Strategy

HeliosAI uses a Blue/Green deployment strategy for the API layer to ensure zero-downtime updates, crucial for a system that must emit real-time WebSocket telemetry uninterrupted.

**Next document:** `53_Monitoring.md`
