# 38 — UI/UX

**HeliosAI** — AI-Powered Space Weather Intelligence Platform
Document 38 of 61

---

## 1. Purpose

Defines the visual design system and interaction principles for HeliosAI's dashboard, ensuring the interface serves its primary user — a scientist or space-weather-desk operator who needs to trust and act on nowcast/forecast triggers quickly, per the README's "Interface with visual alerts" requirement.

---

## 2. Design Principles

1. **Legibility under urgency** — flare alerts must be readable at a glance; color and shape encode severity redundantly (not color alone), for accessibility.
2. **Data density without clutter** — dual-band light curves, hardness ratio, and forecast probability share a coordinated timeline without overwhelming the viewer.
3. **Trust through transparency** — every alert links directly to its supporting evidence (raw light curve, explainability output), never a bare notification.
4. **Progressive disclosure** — overview first, drill-down on demand (catalogue summary → single-event detail → raw data + SHAP/attention view).

---

## 3. Color System (Flare-Class Severity)

| Flare Class (GOES-equivalent) | Color Token | Usage |
|---|---|---|
| A / B (low) | `--severity-low` (blue-gray) | Catalogue rows, minor banner |
| C (moderate) | `--severity-moderate` (amber) | Catalogue rows, standard banner |
| M (high) | `--severity-high` (orange) | Prominent banner, sound-optional alert |
| X (extreme) | `--severity-extreme` (red) | Full-width banner, persistent until acknowledged |
| Tentative / single-band only | `--severity-tentative` (dashed outline, neutral gray) | Distinguishes unconfirmed dual-band candidates per README's cross-validation design |

Color is always paired with an icon/shape (circle/triangle/diamond/octagon of increasing severity) so the system remains usable for color-vision-deficient users.

---

## 4. Core Screens

| Screen | Purpose | Primary Component |
|---|---|---|
| Live Dashboard | Real-time dual-band light curves + active alert banner | `dcc.Graph` (Plotly) + WebSocket-driven banner |
| Catalogue Explorer | Browse/filter/export historical nowcast & forecast events | Dash AG Grid |
| Event Detail | Single flare deep-dive: raw curves, class, confidence, explainability | Composite of Plotly + SHAP/attention plots |
| Alert Console | Acknowledge/annotate active and past alerts | Card list + action buttons |
| Admin Panel | User/role management, thresholds, ingestion status | Streamlit forms |

---

## 5. Interaction Patterns

- **Alert lifecycle:** `triggered → acknowledged → resolved`, always visible as a status chip; unacknowledged alerts persist across page navigation.
- **Zoom/pan on light curves:** synchronized across SoLEXS and HEL1OS panels (shared x-axis), so a zoom on one band zooms both.
- **Hover tooltips:** show raw flux, timestamp, and (if within a flare window) class and confidence — never just a bare number.
- **Filtering:** catalogue filters (class, band, confidence, date range, tentative/confirmed) are URL-encoded, so filtered views are shareable/bookmarkable.

---

## 6. Layout Grid

Standard 12-column responsive grid (Dash Bootstrap Components), collapsing to a stacked single-column layout below 768px for tablet-based mission-desk displays.

---

## 7. Accessibility

- WCAG 2.1 AA contrast minimums for all text and severity indicators.
- All interactive elements keyboard-navigable (Dash's underlying React runtime provides this out of the box; verified via automated `pytest` + `axe-core` checks in CI).
- Alert sounds (optional, for M/X class) are user-toggleable and never the sole signal of an event.

---

## 8. Interfaces to Other Documents

- **`37_Frontend_Architecture.md`** — technical structure this design is implemented within.
- **`39_Dashboard.md`** — detailed spec of the Live Dashboard screen.
- **`42_Alert_System.md`** — alert lifecycle and dispatch logic behind the Alert Console.
- **`29_Explainable_AI.md`** — content shown in the Event Detail explainability panel.

---

**Next document:** `39_Dashboard.md` — say **NEXT** to continue.
