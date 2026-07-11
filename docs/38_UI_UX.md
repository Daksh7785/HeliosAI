# 38 — UI/UX Design Principles

> **Document 38 of 61** in the HeliosAI documentation set (see `README.md` → Repository Structure). Defines the visual and interaction design rules for the Dashboard.

---

## Table of Contents

1. [Purpose of This Document](#purpose-of-this-document)
2. [Design Philosophy](#design-philosophy)
3. [Color Palette and Theming](#color-palette-and-theming)
4. [Accessibility](#accessibility)

---

## Purpose of This Document

This document ensures the HeliosAI dashboard remains legible and professional, avoiding the cluttered "academic notebook" look common in scientific toolkits.

## Design Philosophy

- **Data-First:** The light curve visualizations (`40_Data_Visualization.md`) should take up 70% of the screen real estate.
- **High-Contrast:** Solar flare spikes happen rapidly; visual contrast must highlight anomalous peaks instantly.
- **Actionable Alerts:** Nowcast and Forecast alerts must appear as toast notifications or banner overlays without obscuring the active data view.

## Color Palette and Theming

The application defaults to a **Dark Theme** to reduce eye strain for operators monitoring screens continuously.
- Background: `#1A1B1E`
- SoLEXS Soft X-ray Trace: Cyan/Blue (`#228BE6`)
- HEL1OS Hard X-ray Trace: Orange/Red (`#FA5252`)
- Alerts (M/X Class): Flashing Red borders.

## Accessibility

- All charts must support hover-text tooltips.
- UI elements must have sufficient contrast ratios (WCAG AA).

**Next document:** `39_Dashboard.md`
