# 54 — Secrets Management

> **Document 54 of 61** in the HeliosAI documentation set (see `README.md` → Repository Structure). Defines how passwords and API keys are protected.

---

## Table of Contents

1. [Purpose of This Document](#purpose-of-this-document)
2. [What Constitutes a Secret?](#what-constitutes-a-secret)
3. [The Vault](#the-vault)
4. [Injecting Secrets](#injecting-secrets)

---

## Purpose of This Document

Hardcoding passwords in Git is a severe security vulnerability. This document defines how HeliosAI manages sensitive configuration.

## What Constitutes a Secret?

- Database passwords (PostgreSQL, Redis).
- The JWT signing key used by FastAPI (`35_Authentication.md`).
- SMTP credentials for the Alert Dispatcher (`42_Alert_Dispatcher.md`).
- AWS/GCP IAM credentials used by Terraform (`50_Infrastructure.md`).

## The Vault

HeliosAI uses HashiCorp Vault (or the cloud provider's native equivalent, like AWS Secrets Manager) as the single source of truth for secrets.

## Injecting Secrets

Secrets are never written to disk within the containers. 
- **Kubernetes:** The External Secrets Operator syncs secrets from the Vault into native Kubernetes `Secret` objects.
- **Pods:** These `Secret` objects are mounted as environment variables (e.g., `DATABASE_URL`) into the FastAPI and Celery pods at runtime.

**Next document:** `55_Disaster_Recovery.md`
