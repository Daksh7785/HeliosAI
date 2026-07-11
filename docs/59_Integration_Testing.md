# 59 — Integration Testing

> **Document 59 of 61** in the HeliosAI documentation set (see `README.md` → Repository Structure). Defines tests spanning multiple services.

---

## Table of Contents

1. [Purpose of This Document](#purpose-of-this-document)
2. [What is an Integration Test?](#what-is-an-integration-test)
3. [TestContainers](#testcontainers)
4. [API Contract Testing](#api-contract-testing)

---

## Purpose of This Document

A function might work perfectly in isolation, but fail when it tries to insert its result into a database with strict constraints. Integration tests catch these boundary failures.

## What is an Integration Test?

In HeliosAI, an integration test evaluates the "plumbing". Examples:
- Does the `ingestion` service successfully write to TimescaleDB?
- Does the `processing` service correctly read from TimescaleDB, compute features, and push them to Redis?
- Can the `api` service read those features from Redis and trigger a model prediction?

## TestContainers

Because these tests require real databases (not mocks), they use the `testcontainers` Python library. Before the Pytest suite runs, `testcontainers` automatically spins up ephemeral Docker containers for PostgreSQL and Redis, runs the tests against them, and then destroys the containers.

## API Contract Testing

FastAPI provides a `TestClient` (based on `httpx`). Integration tests use this client to hit the `/api/v1/...` endpoints and verify that the JSON responses match the exact OpenAPI schemas defined in `32_API_Design.md`, ensuring the Dashboard doesn't crash due to a missing field.

**Next document:** `60_Performance_Testing.md`
