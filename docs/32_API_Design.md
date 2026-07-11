# 32 — API Design

> **Document 32 of 61** in the HeliosAI documentation set (see `README.md` → Repository Structure). Specifies the RESTful interfaces exposed by the Backend Architecture.

---

## Table of Contents

1. [Purpose of This Document](#purpose-of-this-document)
2. [API Versioning and Standards](#api-versioning-and-standards)
3. [Core Endpoints](#core-endpoints)
4. [Request and Response Schemas](#request-and-response-schemas)
5. [Error Handling](#error-handling)

---

## Purpose of This Document

This document defines the exact REST API routes served by the `services/api/` module. These routes are consumed by the Dashboard (`39_Dashboard.md`), CLI (`24_CLI.md`), and external researchers.

## API Versioning and Standards

- **Base URL:** `/api/v1/`
- **Documentation:** Automated Swagger UI accessible at `/api/v1/docs`.
- **Format:** All requests and responses are strictly JSON.

## Core Endpoints

### 1. Light Curves (`/lightcurves`)
- `GET /lightcurves/solexs`: Retrieve SoLEXS flux. Supports `start_time`, `end_time`, and `downsample` query params.
- `GET /lightcurves/hel1os`: Retrieve HEL1OS flux.
- `GET /lightcurves/fused`: Retrieve the synchronized, feature-engineered dataset including hardness ratio.

### 2. Flare Catalogue (`/catalogue`)
- `GET /catalogue`: List nowcasted events. Filterable by `class_min` (e.g., "M1.0") and `time_range`.
- `GET /catalogue/{event_id}`: Detailed metadata for a specific flare event.

### 3. Forecasts (`/forecasts`)
- `GET /forecasts/latest`: Returns the most recently computed probabilities for 15m, 30m, and 60m horizons.
- `GET /forecasts/history`: Returns historical probabilities to overlay against the actual catalogue for retrospective analysis.

### 4. Explainability (`/explanations`)
- `GET /explanations/{forecast_id}`: Returns SHAP or Captum matrices corresponding to a specific prediction.

## Request and Response Schemas

All payloads are validated using Pydantic models located in `shared/schemas/`. 
Example response for `/forecasts/latest`:
```json
{
  "timestamp": "2024-05-10T14:30:00Z",
  "horizon_15m": {"prob_M": 0.85, "prob_X": 0.12},
  "horizon_30m": {"prob_M": 0.70, "prob_X": 0.05}
}
```

## Error Handling

The API adheres to standard HTTP status codes:
- `400 Bad Request`: Validation failure (caught by Pydantic).
- `401 Unauthorized`: Missing or invalid JWT.
- `404 Not Found`: E.g., querying an `event_id` that does not exist.
- `500 Internal Server Error`: Generic fallback, mapped to `shared/exceptions/errors.py`.

**Next document:** `33_WebSocket_System.md`
