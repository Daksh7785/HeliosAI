# 28 — Transformer Models

> **Document 28 of 61.** Details the third and most advanced model generation in the Forecasting Engine's progression — Informer, PatchTST, and Temporal Fusion Transformer — following `27_Deep_Learning.md`. Closes out the Intelligence Subsystem's model-family documents before `29_Explainable_AI.md`.

---

## Table of Contents
1. [Purpose](#purpose)
2. [Why Transformer-Family Models](#why-transformer-family-models)
3. [Informer](#informer)
4. [PatchTST](#patchtst)
5. [Temporal Fusion Transformer](#temporal-fusion-transformer)
6. [Model Selection Process](#model-selection-process)
7. [Revision History](#revision-history)

---

## Purpose

Specifies HeliosAI's highest-capacity forecasting model tier, targeting the longest-range precursor patterns per `README.md` → Objectives, and the literature basis established in `12_Research_Background.md`.

---

## Why Transformer-Family Models

Standard point-wise self-attention scales poorly with long input sequences and doesn't inherently exploit the local, patch-like structure of time-series precursor windows. The three architectures below each address a specific limitation relevant to HeliosAI's forecasting lookback windows (per `21_Feature_Engineering.md`).

---

## Informer

Uses ProbSparse self-attention to make attention computation tractable over long input sequences — relevant since HeliosAI's forecasting lookback windows may need to span longer pre-flare periods than an LSTM/GRU can practically model. Evaluated first in this generation as the most general-purpose long-sequence option.

---

## PatchTST

Segments the input sequence into patches before applying attention, improving both efficiency and — per the literature in `12_Research_Background.md` — accuracy for long-horizon forecasting relative to point-wise attention. A natural fit given HeliosAI's rolling-window feature construction already operates on windowed sub-sequences.

---

## Temporal Fusion Transformer

Combines recurrent components with attention and includes built-in interpretability (variable selection networks, attention-weight outputs) — directly supporting the explainability requirement in `README.md` and `29_Explainable_AI.md`, since TFT's attention weights can be surfaced to scientists without a separate post-hoc explainability pass.

---

## Model Selection Process

All three architectures are trained and evaluated under the identical protocol used for `26_Machine_Learning.md` and `27_Deep_Learning.md` (time-based splits, per-class precision/recall, calibration, empirical lead time). The final production forecasting model is whichever generation/architecture wins on held-out historical events — not assumed in advance to be the most complex option. Results and the selection rationale are documented in `48_Model_Evaluation.md` and ultimately `59_Research_Paper.md`.

**Next document:** `29_Explainable_AI.md` — say **NEXT** to continue.

---

## Revision History
| Version | Date | Author | Notes |
|---|---|---|---|
| 0.1 | 2026-07-12 | HeliosAI Documentation | Initial Transformer-family model spec — Informer, PatchTST, TFT rationale and selection process |
