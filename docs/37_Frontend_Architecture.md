# 37 — Frontend Architecture

> **Document 37 of 61** in the HeliosAI documentation set (see `README.md` → Repository Structure). Defines the Dash-based client macro-architecture.

---

## Table of Contents

1. [Purpose of This Document](#purpose-of-this-document)
2. [Technology Choice](#technology-choice)
3. [App Structure](#app-structure)
4. [State Management](#state-management)

---

## Purpose of This Document

This document defines the `services/dashboard/` module. It translates the 100%-Python requirement into a responsive, real-time web interface.

## Technology Choice

- **Framework:** Plotly Dash. Chosen because it provides complex, interactive data visualizations (which are critical for light curves) natively in Python without requiring a separate React/TypeScript layer.
- **Components:** Dash Mantine Components (DMC) for modern UI elements (buttons, notifications, layout grids) that look better than default Dash HTML components.

## App Structure

The dashboard is structured as a multi-page Dash application:
- `app.py`: The entrypoint and layout shell.
- `pages/`: Individual route handlers (e.g., Live Dashboard, Catalogue, Admin).
- `api_client/`: A module dedicated to wrapping HTTPX/Requests calls to the `services/api/` layer, ensuring the dashboard never talks to the database directly.

## State Management

Since Dash is stateless by design, state (such as the currently selected time range or the user's JWT) is stored in:
- `dcc.Store` (browser local storage) for tokens.
- URL query parameters (for shareable links to specific flare events).

**Next document:** `38_UI_UX.md`
