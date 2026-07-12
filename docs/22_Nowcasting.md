# 22 — Nowcasting

**HeliosAI** — AI-Powered Space Weather Intelligence Platform
Document 22 of 61

---

## 1. Purpose
Defines the algorithmic methodology for real-time nowcasting of solar flares using combined SoLEXS and HEL1OS data, resolving the P0-4 blocker.

---

## 2. Methodology
The nowcasting engine detects active solar flares by comparing real-time flux against a dynamic baseline:
1. **Dynamic Baseline**: Uses a rolling median over a configurable time window (e.g., 5 minutes) to establish the background flux.
2. **Median Absolute Deviation (MAD)**: Computes the rolling MAD to measure background volatility.
3. **Trigger Threshold**: A flare candidate is flagged when the real-time flux exceeds the baseline by `N * MAD` (where N is typically 5) and surpasses a hardcoded absolute noise floor.

---

## 3. Dual-Band Fusion
- **SoLEXS (Soft X-rays)**: Provides the duration and absolute class mapping (C, M, X class logic) of the flare.
- **HEL1OS (Hard X-rays)**: Often exhibits impulsive peaks *before* or *during* the early phase of the soft X-ray peak.
- **Master Trigger**: The system triggers if *either* band crosses the dynamic threshold, taking advantage of HEL1OS's impulsiveness.

**Next document:** `23_Forecasting.md` — say **NEXT** to continue.
