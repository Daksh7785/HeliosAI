# 25 — Hybrid AI System

> **Document 25 of 61.** Explains why HeliosAI is a *hybrid* system — combining rule-based/statistical methods with learned models — rather than a single end-to-end model, extending `24_AI_Architecture.md` before the model-family deep-dives in `26`–`28`.

---

## Table of Contents
1. [Purpose](#purpose)
2. [Why Not a Single End-to-End Model](#why-not-a-single-end-to-end-model)
3. [Where Each Paradigm Is Used](#where-each-paradigm-is-used)
4. [Interoperability Contract](#interoperability-contract)
5. [Fallback Behavior](#fallback-behavior)
6. [Revision History](#revision-history)

---

## Purpose

Documents the deliberate architectural choice, already implicit in `08_Development_Roadmap.md`'s Design Decisions, to keep statistical detection (nowcasting) and learned prediction (forecasting) as distinct paradigms working together, rather than replacing both with one large model.

---

## Why Not a Single End-to-End Model

1. **Interpretability** — a single opaque model mapping raw light curves directly to alerts would be far harder to audit than statistical detection + explainable learned forecasting, undermining the trust requirement in `README.md`'s Design Decisions.
2. **Failure isolation** — a bug or drift in the forecasting model cannot corrupt the master catalogue, since nowcasting doesn't depend on forecasting's output.
3. **Data efficiency** — nowcasting's statistical methods require no training data and work from day one; forecasting's learned models require the catalogue nowcasting builds up over time. A single joint model would need both pieces to exist simultaneously to bootstrap.
4. **Evaluation clarity** — the Problem Statement's evaluation criteria (TPR/FAR, lead time) map cleanly onto two separately-measurable engines rather than one conflated metric.

---

## Where Each Paradigm Is Used

| Task | Paradigm | Why |
|---|---|---|
| Flare detection (nowcasting) | Statistical (threshold + changepoint) | No training data dependency; fast; interpretable by construction |
| Flare classification (class bin) | Rule-based (flux-to-class mapping) | GOES-equivalent standard, not a learned quantity |
| Flare probability forecasting | Learned (ML/DL, per `26`–`28`) | Precursor patterns are too complex for fixed rules to capture reliably |
| Confidence fusion (cross-band) | Rule-based, tunable weights | Interpretability requirement for scientific trust |

---

## Interoperability Contract

The forecasting engine treats the nowcasting engine strictly as a **label source** via the master catalogue's documented schema (`30_Database_Design.md`) — it never reaches into nowcasting's internal detection logic. This keeps the two engines independently replaceable; e.g., a future changepoint algorithm swap in nowcasting does not require retraining forecasting models, provided the catalogue schema is unchanged.

---

## Fallback Behavior

If the forecasting engine is unavailable (model registry issue, retraining in progress), the nowcasting engine continues operating independently — the system degrades to nowcast-only rather than failing entirely, satisfying the Reliability NFR in `README.md`.

**Next document:** `26_Machine_Learning.md` — say **NEXT** to continue.

---

## Revision History
| Version | Date | Author | Notes |
|---|---|---|---|
| 0.1 | 2026-07-12 | HeliosAI Documentation | Initial Hybrid AI System rationale and interoperability contract established |
