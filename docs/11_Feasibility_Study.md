# 11 — Feasibility Study

> **Document 11 of 61** in the HeliosAI documentation set (see `README.md` → Repository Structure). Cross-checks the roadmap (`08`), timeline (`09`), and risk register (`10`) against whether the project is actually achievable as scoped. Precedes `12_Research_Background.md`.

---

## Table of Contents

1. [Purpose of This Document](#purpose-of-this-document)
2. [Feasibility Dimensions Assessed](#feasibility-dimensions-assessed)
3. [Technical Feasibility](#technical-feasibility)
4. [Data Feasibility](#data-feasibility)
5. [Resource / Team Feasibility](#resource--team-feasibility)
6. [Operational Feasibility](#operational-feasibility)
7. [Economic / Cost Feasibility](#economic--cost-feasibility)
8. [Schedule Feasibility](#schedule-feasibility)
9. [Overall Feasibility Verdict](#overall-feasibility-verdict)
10. [Revision History](#revision-history)

---

## Purpose of This Document

`08` and `09` assumed the project *is* buildable in the sequence and timeframe described, and `10` catalogued what could go wrong. This document steps back and asks the harder question directly: **is HeliosAI, as scoped, actually feasible** for the team and constraints implied by the README — and if any dimension is marginal, what has to be true for it to work.

---

## Feasibility Dimensions Assessed

| Dimension | Verdict | Confidence |
|---|---|---|
| Technical | Feasible | High |
| Data | Feasible with caveats | Medium |
| Resource / Team | Feasible with AI-assisted acceleration | Medium |
| Operational | Feasible (research-grade, not operational-grade) | High |
| Economic / Cost | Feasible on modest infrastructure budget | High |
| Schedule | Feasible with buffer already applied | Medium |

---

## Technical Feasibility

**Question:** Can the described architecture actually be built with the chosen tech stack?

- Every component in `07_Tech_Stack.md`'s all-Python stack (FastAPI, Dash, PostgreSQL/TimescaleDB, Celery/Redis, MLflow, PyTorch) is mature, widely documented, and has no known blocking incompatibility with the others.
- Dual-band fusion, changepoint detection, and sequence-to-probability forecasting are all established techniques in the space-weather and time-series literature (see `12_Research_Background.md` for citations) — HeliosAI is engineering these into a cohesive pipeline, not inventing new algorithmic theory.
- The riskiest technical component is the Transformer-family forecasting models (Informer/PatchTST/TFT), but classical ML baselines (Phase 4 in `08`) provide a technically-guaranteed fallback if deep models underperform or overrun.

**Verdict: Technically feasible**, with deep-model performance being the only genuinely open question (addressed empirically during Phase 4, not assumed away).

---

## Data Feasibility

**Question:** Does sufficient, accessible data exist to train and validate the system?

- SoLEXS and HEL1OS Level-1 data exists and is nominally accessible via ISSDC PRADAN, per the Problem Statement itself.
- **Caveat (ties to R1 in `10_Risk_Assessment.md`):** portal access is often session/credential-gated, which is why manual-drop ingestion is a first-class design decision rather than a convenience feature.
- **Caveat (ties to R2 in `10_Risk_Assessment.md`):** high-class (M/X-equivalent) flare events are inherently rare in any solar dataset; Aditya-L1's operational history to date may not provide many examples. GOES XRS supplementary data (already in-scope per `README.md`) partially mitigates this by extending the labeled-event pool.
- No proprietary or newly-collected data is required — this is a strength for feasibility, since the project doesn't depend on new instrumentation or a data-collection campaign.

**Verdict: Feasible with caveats** — contingent on manual-drop ingestion working reliably and on GOES supplementation being sufficient for minority-class training.

---

## Resource / Team Feasibility

**Question:** Can a small team realistically deliver this scope?

- The scope (61 documents, dual-band signal processing, two ML/DL model tracks, full REST/WebSocket API, Python-native dashboard, MLOps stack) is large for a 2–4 person team under a conventional development model.
- **This is explicitly why the Antigravity Master Prompt structure exists** (per `README.md` → Implementation Details and `08` → Design Decisions): each subsystem gets a context-isolated prompt enabling AI-assisted implementation without cross-module context bleed, meaningfully changing the achievable scope-per-person.
- Risk R8 (`10_Risk_Assessment.md`) already flags this as a Score-12 risk — feasibility here is **conditional on that mitigation actually working in practice**, which should be validated early (Sprint 1–2) rather than assumed for the full build.
- Open-source (GSSoC-style) contribution, listed under Future Scope in `README.md`, is a plausible *additional* lever if the core team needs more throughput, but is not assumed as a Phase 1–8 dependency.

**Verdict: Feasible, conditionally** — the AI-assisted, module-isolated workflow is not optional overhead here; it is load-bearing for team-size feasibility.

---

## Operational Feasibility

**Question:** Once built, can the system actually be run and maintained by its intended users?

- The system is explicitly scoped as **research/decision-support**, not mission-critical/human-life-safety certified (per `README.md` → Scope: Out of Scope). This significantly lowers the operational bar relative to an operational space-weather warning system.
- `docker compose up --build` as the target deployment path (per `README.md` → Getting Started) is realistic for a research group's infrastructure — no Kubernetes cluster is required for baseline operation (Kubernetes is listed as optional, scale-out only, in `07_Tech_Stack.md`).
- Authentication/authorization for multi-user research deployments is already scoped, making the system usable by more than one scientist without additional operational redesign.

**Verdict: Feasible** for its stated research/decision-support purpose; would require additional operational feasibility work (SLA hardening, uptime guarantees) only if repurposed toward operational/certified use, which is explicitly out of scope.

---

## Economic / Cost Feasibility

**Question:** Is the infrastructure cost proportionate to a research-group budget?

- All core infrastructure (PostgreSQL/TimescaleDB, Redis, FastAPI, Dash, MLflow) is open-source with no licensing cost.
- Compute cost is dominated by deep-model training (GPU time for Transformer-family models); this can be scoped down to CPU-feasible baselines (Phase 4 baselines) if GPU budget is constrained, without abandoning the forecasting capability entirely.
- No paid third-party API dependency is required for the core pipeline (PRADAN and GOES data are both freely accessible research datasets).

**Verdict: Feasible** on a modest research infrastructure budget; GPU access is the only cost variable worth planning for explicitly ahead of Phase 4.

---

## Schedule Feasibility

**Question:** Is the ~15-sprint (with buffer) estimate in `09_Project_Timeline.md` realistic?

- The estimate already incorporates buffer specifically at the two highest-uncertainty points (post-Phase-4 deep model tuning, pre-Phase-8 acceptance testing), which is good practice rather than optimism.
- Schedule feasibility is most sensitive to **R1 (PRADAN access)** and **R8 (team size)** from `10_Risk_Assessment.md` — both are structural risks to the sprint estimate, not just to individual phases.
- **Verdict: Feasible as a planning estimate**, but should be explicitly re-baselined after Sprint 2 (per `09_Project_Timeline.md`'s own tracking cadence) once real ingestion-path velocity is known.

---

## Overall Feasibility Verdict

**HeliosAI is feasible to build as scoped**, provided two conditions hold, both of which are already designed for rather than left to chance:

1. **Manual-drop ingestion must work reliably** as the primary (not merely fallback) data path, given PRADAN's credential-gating.
2. **The Antigravity Master Prompt / AI-assisted implementation workflow must genuinely offset the team-size-vs-scope gap** — this should be validated on the first 1–2 modules before committing to the full 8-phase build at the estimated pace.

No dimension assessed here produces a "not feasible" verdict; the caveats above are the specific things to watch, not reasons to change scope.

---

## Revision History

| Version | Date | Author | Notes |
|---|---|---|---|
| 0.1 | 2026-07-12 | HeliosAI Documentation (Antigravity workflow) | Initial Feasibility Study — technical, data, resource, operational, economic, and schedule feasibility assessed |
