# 32 — API Design

**HeliosAI** — AI-Powered Space Weather Intelligence Platform
Document 32 of 61

---

## 1. Purpose
Defines the REST API contract for HeliosAI, resolving the P0-2 blocker identified in the Final Review Report. This API enables frontend clients to query telemetry, catalogue entries, and forecasting probabilities.

---

## 2. Base URL & Versioning
- **Base Path**: `/api/v1`
- **Versioning Policy**: Semantic versioning. Minor backwards-compatible additions to v1; breaking changes will introduce v2.

---

## 3. Endpoints

### 3.1 Telemetry & Features
- **`GET /api/v1/telemetry/recent`**
  - **Description**: Returns recent fused telemetry and feature store data.
  - **Query Params**: `limit` (int, default=100)
  - **Response**: Array of FeatureResponse (`timestamp`, `solexs_flux`, `hel1os_flux`, `forecast_probability`, `is_flare_candidate`)

### 3.2 Catalogue
- **`GET /api/v1/catalogue/recent`**
  - **Description**: Returns recently detected or promoted flares.
  - **Query Params**: `limit` (int, default=10)
  - **Response**: Array of CatalogueResponse (`start_time`, `peak_flux`, `class_level`)

### 3.3 Forecasts
- **`GET /api/v1/forecast/recent`**
  - **Description**: Returns recent forecast probabilities for upcoming flares.
  - **Response**: Time-series of upcoming probability scores.

---

## 4. Authentication
Gated behind JWT authorization as defined in `35_Authentication.md`.

**Next document:** `33_WebSocket_System.md` — say **NEXT** to continue.
