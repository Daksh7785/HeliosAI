# 40 — Data Visualization

**HeliosAI** — AI-Powered Space Weather Intelligence Platform
Document 40 of 61

---

## 1. Purpose

Specifies how HeliosAI renders high-frequency, potentially multi-day X-ray light-curve data efficiently and accurately in the browser, without misleading the viewer during down-sampling.

---

## 2. Rendering Stack

| Layer | Technology |
|---|---|
| Charting library | Plotly.py (WebGL-accelerated `scattergl` traces for long series) |
| Server-side aggregation | Pandas + custom down-sampling utilities |
| Down-sampling algorithm | **LTTB** (Largest-Triangle-Three-Buckets), preserves visual shape/peaks better than naive decimation |
| Delivery format | JSON payloads over REST (initial load) and WebSocket (incremental) |

---

## 3. Down-Sampling Strategy

Raw SoLEXS/HEL1OS cadence can produce far more points than a screen can usefully render. HeliosAI applies resolution tiers based on the selected time range:

| View Range | Target Points Rendered | Strategy |
|---|---|---|
| ≤ 1 hour | Full resolution | No down-sampling |
| 1–24 hours | ~5,000 points | LTTB per band |
| > 24 hours | ~5,000 points | LTTB per band, with peak-preservation override (flare peaks are never dropped even if LTTB would otherwise smooth them out) |

**Peak-preservation override:** before down-sampling, any point already flagged as part of a nowcasted flare event (per the master catalogue) is force-included, guaranteeing that zooming out never visually hides a real event — a direct safeguard against the false impression of "no activity" during a high-density flare period.

---

## 4. Dual-Band Synchronization

Both SoLEXS and HEL1OS traces share a single x-axis (UTC, post-time-synchronization per `19_Data_Synchronization.md`). Zoom/pan/hover events on one trace are mirrored to the other via a shared Dash callback, so a scientist can visually correlate soft/hard X-ray timing offsets — directly supporting the hardness-ratio feature's interpretability.

---

## 5. Explainability Overlays

When viewing a specific event's detail page, the light curve is annotated with:
- Detected onset, peak, and decay-end markers (from the nowcasting engine).
- Forecast trigger point, if the event was preceded by a forecast alert, with a lead-time annotation (predicted → actual peak).
- SHAP/attention-weight highlight regions from `29_Explainable_AI.md`, shown as a secondary shaded trace beneath the main curve.

---

## 6. Chart Types Used

| Chart | Where Used |
|---|---|
| Line (log-scale y-axis) | Primary light curves — flux spans orders of magnitude |
| Shaded region | Flare event windows, confidence bands |
| Radial gauge | Live forecast probability |
| Heatmap | Catalogue Explorer's flare-class-over-time overview |
| Bar (stratified) | Model evaluation class-wise precision/recall (`48_Model_Evaluation.md`) |

---

## 7. Accuracy Safeguards

- Y-axis is always log-scale by default for flux (matches domain convention; linear toggle available), with axis labels never silently rescaled without a visible unit change.
- Down-sampled views carry a subtle "aggregated view" indicator; switching to full resolution is one click (zoom-to-range).

---

## 8. Interfaces to Other Documents

- **`39_Dashboard.md`** — primary consumer of these visualization patterns.
- **`21_Feature_Engineering.md`** — source of hardness ratio and other overlay features.
- **`29_Explainable_AI.md`** — source of explainability overlay data.
- **`43_Analytics.md`** — aggregate/statistical views built on the same charting stack.

---

**Next document:** `41_Admin_Panel.md` — say **NEXT** to continue.
