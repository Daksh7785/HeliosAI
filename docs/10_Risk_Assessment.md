# 10 — Risk Assessment

> **Document 10 of 61** in the HeliosAI documentation set (see `README.md` → Repository Structure). Formalizes risks flagged informally in `08_Development_Roadmap.md` (Risk Checkpoints) and `09_Project_Timeline.md` (Critical Path). Precedes `11_Feasibility_Study.md`.

---

## Table of Contents

1. [Purpose of This Document](#purpose-of-this-document)
2. [Risk Scoring Method](#risk-scoring-method)
3. [Risk Register](#risk-register)
4. [Top Risks — Detail](#top-risks--detail)
5. [Risk Heat Map](#risk-heat-map)
6. [Monitoring & Review Cadence](#monitoring--review-cadence)
7. [Revision History](#revision-history)

---

## Purpose of This Document

This document consolidates every risk surfaced during architecture and planning (`03`–`09`) into a single, scored register, so that:

- Mitigation ownership is explicit before implementation begins.
- The timeline in `09_Project_Timeline.md` can be re-validated against realistic risk-adjusted slippage.
- Downstream Antigravity Master Prompts can bake mitigations directly into module scope rather than discovering them mid-build.

---

## Risk Scoring Method

Each risk is scored on two axes, 1 (lowest) to 5 (highest):

- **Likelihood** — how probable the risk is to materialize during this project.
- **Impact** — how severely it would affect schedule, scientific validity, or the Acceptance Criteria in `README.md` if it materializes.

**Risk Score = Likelihood × Impact** (max 25). Scores ≥15 are treated as top risks requiring an explicit, named mitigation before the dependent phase starts.

---

## Risk Register

| ID | Risk | Phase(s) Affected | Likelihood | Impact | Score | Owner Area |
|---|---|---|---|---|---|---|
| R1 | ISSDC PRADAN automated access unavailable or heavily rate-limited | Phase 1 | 4 | 5 | 20 | Ingestion |
| R2 | Insufficient historical high-class (M/X-equivalent) flare events for robust minority-class training | Phase 4 | 4 | 4 | 16 | Intelligence |
| R3 | Deep sequence model (Transformer-family) tuning takes longer than estimated | Phase 4 | 4 | 3 | 12 | Intelligence |
| R4 | Cross-band time synchronization drift between SoLEXS and HEL1OS clocks | Phase 2 | 3 | 4 | 12 | Processing |
| R5 | Dual-band fusion gate over-suppresses genuine single-band-only low-class flares | Phase 3 | 3 | 4 | 12 | Intelligence |
| R6 | TimescaleDB hypertable performance degradation at high-cadence, multi-year data volumes | Phase 2, 7 | 2 | 4 | 8 | Data Layer |
| R7 | Lead-time metric misinterpreted/misreported if not computed strictly empirically | Phase 4, 8 | 2 | 5 | 10 | Intelligence |
| R8 | Small team size vs. 61-document + full-stack build scope | All | 3 | 4 | 12 | Program |
| R9 | Dash/Streamlit dual-framework maintenance overhead | Phase 6 | 2 | 2 | 4 | Experience |
| R10 | Secrets/credentials mismanagement across Docker/CI environments | Phase 7 | 2 | 5 | 10 | Security |
| R11 | Open-source contributor onboarding friction (if GSSoC-style workflow adopted) | Phase 6, 7 | 3 | 2 | 6 | Program |
| R12 | GOES XRS supplementary data schema or availability changes | Phase 1, 3 | 2 | 3 | 6 | Ingestion |

---

## Top Risks — Detail

### R1 — PRADAN Automated Access (Score: 20)
**Description:** ISSDC PRADAN portal access is often session/credential-gated per-user, as already noted in `README.md`'s Scope section. Programmatic/token-based access may not be available for all account tiers.
**Mitigation:** Manual-drop ingestion mode (`data/raw/` watched directory) is built as a **first-class path, not a fallback**, per `README.md` → Implementation Details. Ingestion Phase 1 explicitly budgets for both paths from the start rather than treating manual-drop as an afterthought.
**Early warning signal:** If automated fetcher authentication fails repeatedly in Sprint 1, escalate immediately rather than continuing to debug — switch primary reliance to manual-drop before Sprint 2 begins.

### R2 — Insufficient High-Class Flare Events (Score: 16)
**Description:** M/X-class solar flares are rare relative to A/B/C-class events; Aditya-L1's operational history may not yet contain enough labeled high-class examples for robust deep-model training.
**Mitigation:** Class-stratified oversampling (SMOTE-style on tabular features, per `README.md` → Objectives) and optional supplementation with GOES XRS historical data for cross-validation and additional labeled examples, as already scoped as in-scope in `README.md`.
**Early warning signal:** Class distribution audit at the end of Phase 3 (master catalogue construction) — if high-class representation is below a usable threshold, flag before Phase 4 forecasting training begins.

### R3 — Deep Model Tuning Overrun (Score: 12)
**Description:** Transformer-family time-series models (Informer, PatchTST, TFT) are the least predictable component to tune, as already flagged in `09_Project_Timeline.md`'s buffer allocation.
**Mitigation:** Baselines (XGBoost/LightGBM/CatBoost) are shipped and evaluated first, so a usable forecasting capability exists even if deep-model tuning overruns; the +1 sprint buffer after Phase 4 absorbs likely overrun.

### R4 — Cross-Band Time Sync Drift (Score: 12)
**Description:** SoLEXS and HEL1OS may have independent onboard clocks; naive alignment could introduce spurious lag in hardness-ratio features.
**Mitigation:** Dedicated Time Synchronization Engine (Phase 2) with explicit spacecraft-time → UTC conversion, validated against known reference events before Cross-Band Fusion Layer is trusted for feature engineering.

### R5 — Fusion Gate Over-Suppression (Score: 12)
**Description:** Requiring dual-band confirmation before catalogue promotion (per `README.md`'s key differentiator) risks discarding genuine single-band-only low-class flares.
**Mitigation:** Already partially addressed by design — single-band detections are **flagged as "tentative"** rather than discarded, per `README.md` → Core Algorithms Summary. This risk register formalizes that tentative-flagged events must still be retained and reviewable, not silently dropped.

### R8 — Small Team vs. Full Scope (Score: 12)
**Description:** A 61-document, full-stack (ingestion → ML → API → dashboard → MLOps) build is a large scope for a small research/engineering team.
**Mitigation:** Antigravity Master Prompt structure (context-isolated, per-module) exists specifically to allow AI-assisted implementation to close this gap without cross-module context bleed, per `README.md` → Implementation Details.

---

## Risk Heat Map

```mermaid
quadrantChart
    title Risk Likelihood vs Impact
    x-axis Low Likelihood --> High Likelihood
    y-axis Low Impact --> High Impact
    quadrant-1 Monitor Closely
    quadrant-2 Critical - Mitigate First
    quadrant-3 Low Priority
    quadrant-4 Contingency Plan Ready
    R1: PRADAN Access: [0.8, 0.9]
    R2: Sparse High-Class Events: [0.7, 0.7]
    R3: Deep Model Tuning: [0.7, 0.5]
    R4: Clock Sync Drift: [0.5, 0.7]
    R5: Fusion Over-Suppression: [0.5, 0.7]
    R6: TimescaleDB Scale: [0.3, 0.7]
    R7: Lead-Time Misreport: [0.3, 0.9]
    R8: Team Size vs Scope: [0.5, 0.7]
    R10: Secrets Mismanagement: [0.3, 0.9]
```

---

## Monitoring & Review Cadence

- Risk register reviewed at the end of every sprint alongside the milestone check-in defined in `09_Project_Timeline.md`.
- Any risk crossing into Score ≥20 territory (currently only R1) triggers a mandatory scope discussion before the next phase's Antigravity Master Prompt is finalized.
- This register will be cross-checked against `11_Feasibility_Study.md` for consistency once that document is drafted.

**Next document:** `11_Feasibility_Study.md` — say **NEXT** to continue.

---

## Revision History

| Version | Date | Author | Notes |
|---|---|---|---|
| 0.1 | 2026-07-12 | HeliosAI Documentation (Antigravity workflow) | Initial Risk Assessment — scored register, top-risk mitigations, and heat map established |
