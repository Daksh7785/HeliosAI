# 24 — Command Line Interface (CLI)

> **Document 24 of 61** in the HeliosAI documentation set (see `README.md` → Repository Structure). Defines the command-line experience for interacting with the HeliosAI platform locally.

---

## Table of Contents

1. [Purpose of This Document](#purpose-of-this-document)
2. [CLI Role in HeliosAI](#cli-role-in-heliosai)
3. [Technology Stack](#technology-stack)
4. [Primary Commands](#primary-commands)
5. [Configuration](#configuration)

---

## Purpose of This Document

This document outlines the design of the HeliosAI Command Line Interface (CLI), establishing how developers and researchers interact with the system without needing the web dashboard.

## CLI Role in HeliosAI

The CLI provides a fast, scriptable interface to the Serving Layer (`32_API_Design.md`). It is primarily used for:
- Querying the latest flares from the nowcasting catalogue.
- Fetching specific forecast probabilities for upcoming time horizons.
- Checking system health and triggering manual ingestion runs.

## Technology Stack

- **Typer / Click:** For robust argument parsing and help-text generation.
- **Rich:** For terminal output formatting (tables, progress bars, colored text).
- **Requests / HTTPX:** For communicating with the REST API.

## Primary Commands

- `heliosai status`: Pings the API health endpoint.
- `heliosai nowcast --last N`: Retrieves the `N` most recent flare events from the catalogue.
- `heliosai forecast --horizon 60m`: Retrieves the latest probability forecasts for the given time horizon.
- `heliosai ingest --manual /path/to/data`: Triggers a manual data ingestion pipeline run for local FITS/CDF files.

## Configuration

The CLI authenticates with the API using a JWT token stored in `~/.heliosai/config.toml` or via the `HELIOSAI_API_KEY` environment variable.

**Next document:** `25_Dashboard_Overview.md`
