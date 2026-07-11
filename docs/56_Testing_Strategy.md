# 56 — Testing Strategy Overview

> **Document 56 of 61** in the HeliosAI documentation set (see `README.md` → Repository Structure). Introduces the QA framework.

---

## Table of Contents

1. [Purpose of This Document](#purpose-of-this-document)
2. [The Testing Pyramid](#the-testing-pyramid)
3. [Test Environments](#test-environments)
4. [Coverage Requirements](#coverage-requirements)

---

## Purpose of This Document

HeliosAI is a scientific instrument as much as a software platform. A bug in the feature engineering pipeline could cause a false alarm that disrupts satellite operations. This document outlines the rigorous testing strategy employed.

## The Testing Pyramid

1. **Unit Tests (Fast):** Testing individual functions (e.g., standard deviation calculation) in isolation (`58_Unit_Testing.md`).
2. **Integration Tests (Medium):** Testing how modules interact (e.g., the API pulling a model from MLflow) (`59_Integration_Testing.md`).
3. **E2E / Performance Tests (Slow):** Simulating a full solar storm data drop and ensuring the system processes it within latency budgets (`60_Performance_Testing.md`).
4. **Data Validation:** Continuous checks on the incoming scientific data (`57_Data_Validation.md`).

## Test Environments

- **Local:** `docker-compose.yaml` spinning up minimal Postgres/Redis instances.
- **CI Pipeline:** GitHub Actions running Pytest on every commit (`52_CI_CD.md`).
- **Staging Cluster:** A replica of production where load testing occurs before a major release.

## Coverage Requirements

The CI pipeline enforces a minimum of **85% test coverage** for all files in `services/`, and **95% coverage** for the `shared/` core logic.

**Next document:** `57_Data_Validation.md`
