# 57 — Data Validation

> **Document 57 of 61** in the HeliosAI documentation set (see `README.md` → Repository Structure). Defines quality control for scientific data.

---

## Table of Contents

1. [Purpose of This Document](#purpose-of-this-document)
2. [Great Expectations](#great-expectations)
3. [Validation Rules](#validation-rules)
4. [Quarantine Protocol](#quarantine-protocol)

---

## Purpose of This Document

Garbage In, Garbage Out. Before data even reaches the model, it must be proven mathematically valid.

## Great Expectations

HeliosAI integrates the `Great Expectations` library at the edge of the Ingestion Subsystem (`17_Data_Ingestion.md`). When a new payload block arrives from PRADAN, it is tested against a declarative suite of "Expectations".

## Validation Rules

Example expectations:
- `expect_column_values_to_not_be_null(column="flux")`
- `expect_column_values_to_be_between(column="flux", min_value=1e-9, max_value=1e-2)`
- `expect_column_values_to_be_increasing(column="timestamp")`

## Quarantine Protocol

If a data block fails validation:
1. It is **not** written to the TimescaleDB hypertable.
2. It is diverted to a `quarantine_bucket` (S3).
3. An alert is sent via the Alert Dispatcher (`42_Alert_Dispatcher.md`).
4. Operators can manually review the block via the Admin Panel (`41_Admin_Panel.md`) to determine if it's a sensor glitch or a parsing error.

**Next document:** `58_Unit_Testing.md`
