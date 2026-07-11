# 58 — Unit Testing

> **Document 58 of 61** in the HeliosAI documentation set (see `README.md` → Repository Structure). Defines the lowest level of software tests.

---

## Table of Contents

1. [Purpose of This Document](#purpose-of-this-document)
2. [Framework and Conventions](#framework-and-conventions)
3. [Mocking External Services](#mocking-external-services)
4. [Testing Data Science Code](#testing-data-science-code)

---

## Purpose of This Document

Unit tests verify that individual atomic functions work exactly as designed.

## Framework and Conventions

- **Framework:** `pytest`
- **Location:** The `tests/unit/` directory mirrors the structure of the `src/` (or microservices) directory.
- **Naming:** Functions must be named `test_<function_name>_<condition>()`.

## Mocking External Services

Unit tests must execute in milliseconds and cannot rely on a running database.
- `unittest.mock` is heavily used to `patch` calls to `sqlalchemy`, `redis`, and `httpx`.
- Fixtures (`conftest.py`) provide standardized mock DataFrame payloads simulating SoLEXS and HEL1OS readings.

## Testing Data Science Code

Testing `scikit-learn` or `pytorch` code is notoriously difficult. HeliosAI's approach:
- We do not unit test the *accuracy* of the model (that is MLOps' job).
- We unit test the *shape* and *types* of the input/output tensors.
- We unit test that the Feature Engineering functions (`21_Feature_Engineering.md`) return the exact expected float values given a static, hardcoded array of inputs.

**Next document:** `59_Integration_Testing.md`
