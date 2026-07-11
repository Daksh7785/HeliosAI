# 27 — Deep Learning

> **Document 27 of 61.** Details the second model generation in the Forecasting Engine's progression (`23_Forecasting.md`): LSTM/GRU sequence models, positioned between the classical baseline (`26_Machine_Learning.md`) and the Transformer-family models (`28_Transformer_Models.md`).

---

## Table of Contents
1. [Purpose](#purpose)
2. [Why This Generation Exists](#why-this-generation-exists)
3. [Architecture](#architecture)
4. [Input Representation](#input-representation)
5. [Training Considerations](#training-considerations)
6. [Comparison Against Baseline](#comparison-against-baseline)
7. [Revision History](#revision-history)

---

## Purpose

Specifies the recurrent deep-sequence-model tier, which directly models the windowed time series rather than a flattened feature vector, testing whether learned temporal representations outperform the hand-engineered baseline from `26`.

---

## Why This Generation Exists

Per `12_Research_Background.md`'s sequence-modeling literature review, LSTM/GRU remain a reasonable, well-understood mid-tier benchmark — simpler and faster to train than Transformer-family architectures, and useful for confirming whether *any* learned sequence representation beats the classical baseline before committing to the higher tuning cost of `28`.

---

## Architecture

- Input: rolling lookback window of raw (lightly-processed, per `18_Data_Preprocessing.md`) per-band flux plus the engineered feature channels from `21_Feature_Engineering.md`, as a multivariate sequence.
- Stacked LSTM or GRU layers (depth tuned empirically) with a final dense layer producing calibrated flare probability and class-probability outputs, consistent with `23_Forecasting.md`'s calibration approach.
- Implemented in PyTorch / PyTorch Lightning (per `07_Tech_Stack.md`), enabling shared training infrastructure with `28`.

---

## Input Representation

Unlike `26`'s flattened feature vector, this generation preserves sequence order explicitly — the model learns temporal dependencies rather than relying solely on pre-computed trend features (`rolling_*_trend` in `21_Feature_Engineering.md`), though those engineered features may still be included as additional input channels rather than discarded.

---

## Training Considerations

- Same time-based split discipline as `26_Machine_Learning.md`, to prevent future-information leakage.
- Same class-imbalance handling philosophy, adapted to sequence models (e.g., weighted loss rather than tabular oversampling, since oversampling individual time steps would break sequence continuity).
- Captum-based explainability (attention/gradient-based, per `29_Explainable_AI.md`) integrated from the start of this generation, not retrofitted.

---

## Comparison Against Baseline

Evaluated on identical held-out historical events and identical metrics as `26_Machine_Learning.md` (per-class precision/recall, calibration, empirical lead time) — this generation is only carried forward into production if it measurably outperforms the classical baseline; otherwise the baseline remains the production forecasting model while this generation's results are documented as a negative/neutral finding, not discarded silently.

**Next document:** `28_Transformer_Models.md` — say **NEXT** to continue.

---

## Revision History
| Version | Date | Author | Notes |
|---|---|---|---|
| 0.1 | 2026-07-12 | HeliosAI Documentation | Initial Deep Learning (LSTM/GRU) spec — architecture, input representation, evaluation against baseline |
