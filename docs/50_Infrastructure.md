# 50 — Infrastructure as Code

> **Document 50 of 61** in the HeliosAI documentation set (see `README.md` → Repository Structure). Defines how the cloud environment is provisioned.

---

## Table of Contents

1. [Purpose of This Document](#purpose-of-this-document)
2. [Why IaC?](#why-iac)
3. [Terraform Structure](#terraform-structure)
4. [Cloud Agnosticism](#cloud-agnosticism)

---

## Purpose of This Document

HeliosAI is not a single script you can run on a laptop; it requires a database, a Redis cache, an MLflow server, Airflow workers, and FastAPI pods. This document explains how those resources are provisioned.

## Why IaC?

To prevent "it works on my machine" syndrome and ensure the staging environment matches production exactly, all infrastructure is defined declaratively using Terraform.

## Terraform Structure

The `infrastructure/terraform/` directory is split into:
- `modules/`: Reusable components (e.g., `postgres_cluster`, `redis_cache`, `eks_cluster`).
- `environments/`: Specific instantiations of those modules (`dev/`, `staging/`, `prod/`).

## Cloud Agnosticism

While currently targeting AWS (EKS, RDS, ElastiCache), the Terraform modules are designed to wrap managed Kubernetes and managed databases, making it relatively straightforward to port to Azure (AKS) or GCP (GKE) if institutional requirements change.

**Next document:** `51_Kubernetes.md`
