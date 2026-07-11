# 12 — Research Background

> **Document 12 of 61** in the HeliosAI documentation set (see `README.md` → Repository Structure). Establishes the scientific and technical literature context behind HeliosAI's design choices. Precedes `13_Space_Weather.md`, which goes deeper into the domain science; this document stays at the "why these methods are credible" level. Feeds forward into `22_Nowcasting.md`, `23_Forecasting.md`, and `28_Transformer_Models.md`, where the methods introduced here are elaborated algorithmically.

---

## Table of Contents

1. [Purpose of This Document](#purpose-of-this-document)
2. [Solar Flare Physics — Background](#solar-flare-physics--background)
3. [X-Ray Flare Classification](#x-ray-flare-classification)
4. [Prior Art in Flare Detection & Nowcasting](#prior-art-in-flare-detection--nowcasting)
5. [Prior Art in Flare Forecasting](#prior-art-in-flare-forecasting)
6. [Sequence Modeling Literature Behind Phase 4](#sequence-modeling-literature-behind-phase-4)
7. [Explainable AI Literature Behind the XAI Layer](#explainable-ai-literature-behind-the-xai-layer)
8. [Gaps HeliosAI Aims to Address](#gaps-heliosai-aims-to-address)
9. [Revision History](#revision-history)

---

## Purpose of This Document

Every major design decision in `08_Development_Roadmap.md` and the algorithm summary in `README.md` rests on established methods rather than novel, unvalidated theory. This document traces those methods back to their scientific and technical origins, so that:

- Reviewers can evaluate HeliosAI's approach against known baselines rather than take design choices on faith.
- `59_Research_Paper.md` (Phase 8 deliverable) has a literature foundation to build on rather than starting from zero.
- Contributors implementing Phase 3/4 modules understand *why* a given technique was chosen, not just *what* to implement.

---

## Solar Flare Physics — Background

Solar flares are sudden brightenings in the solar atmosphere caused by the rapid release of magnetic energy stored in stressed coronal magnetic field structures, typically above active regions with complex sunspot groupings. The released energy accelerates particles and heats plasma, producing enhanced emission across the electromagnetic spectrum — including the soft and hard X-ray bands that SoLEXS and HEL1OS observe.

- **Soft X-ray emission** (roughly 1–15 keV, SoLEXS's band) traces thermal plasma heated during and after the flare, and is the traditional basis of the GOES flare classification scheme.
- **Hard X-ray emission** (HEL1OS's higher-energy band) is associated with non-thermal, accelerated electron populations, typically peaking earlier in a flare's timeline than the soft X-ray thermal peak — a timing offset that is directly exploitable as a precursor signal, and is the physical justification for HeliosAI's hardness-ratio feature.

This soft/hard timing relationship is the scientific basis for why **combining** the two bands (rather than using either alone) is expected to improve both detection confidence and forecast lead time — it is not simply a data-fusion convenience, it reflects the underlying flare energy-release physics.

---

## X-Ray Flare Classification

The GOES flare classification scheme (A/B/C/M/X, each an order of magnitude apart in peak soft X-ray flux, with numeric sub-classing e.g. M2.4) is the de facto global standard for flare magnitude reporting, used operationally by agencies including NOAA's Space Weather Prediction Center. HeliosAI adopts GOES-equivalent binning (as stated in `README.md` → Executive Summary and Objectives) so that:

- Flare-class outputs are immediately interpretable by any space-weather scientist, without requiring familiarity with an Aditya-L1-specific scale.
- Cross-validation against GOES XRS data (already in-scope per `README.md`) is possible without a unit-conversion research project of its own.

---

## Prior Art in Flare Detection & Nowcasting

Automated flare detection in X-ray light curves has historically used two broad families of methods, both of which inform HeliosAI's Phase 3 design:

1. **Threshold/peak-finding methods** — flag a flare when flux crosses a background-relative threshold, then characterize rise/peak/decay. Simple, interpretable, and the traditional basis for real-time operational alerting (e.g., GOES-based NOAA alerts). HeliosAI's per-band detector in `22_Nowcasting.md` builds on this family.
2. **Changepoint detection methods** — statistically identify a shift in the underlying signal's regime (mean, slope, or variance), which can catch flare onsets that a fixed threshold might miss for low-class events. HeliosAI runs this alongside threshold-based detection per band, rather than choosing one over the other, to improve sensitivity to A/B-class flares specifically.

**HeliosAI's differentiator** relative to typical single-band detectors is the **cross-band confidence fusion gate** (per `README.md`'s stated key differentiator) — requiring independent corroboration across SoLEXS and HEL1OS bands before full catalogue promotion, while still retaining single-band-only detections as "tentative" rather than discarding them (addressing Risk R5 in `10_Risk_Assessment.md`).

---

## Prior Art in Flare Forecasting

Flare forecasting approaches in the space-weather literature broadly fall into three generations, all of which appear in HeliosAI's Phase 4 model progression:

1. **Statistical/climatological models** — historically used flare-productivity statistics of active regions (e.g., McIntosh sunspot classification) rather than light-curve precursors directly. HeliosAI does not rely on this generation, since it targets light-curve-based precursor patterns specifically, per the Problem Statement's framing.
2. **Classical machine learning on engineered features** — gradient-boosted trees (as HeliosAI uses for its Phase 4 baseline) trained on hand-engineered features such as flux gradients and spectral ratios. This generation offers strong interpretability and a fast, reliable benchmark, which is why it is sequenced *before* deep models in the roadmap.
3. **Deep sequence models** — LSTM/GRU and, more recently, Transformer-family architectures directly modeling the raw or lightly-processed time series, capturing longer-range temporal dependencies that hand-engineered features may miss. This is the generation HeliosAI's deep-learning track targets for its highest-lead-time forecasts.

A recurring theme across this literature, and one HeliosAI treats as non-negotiable (per Risk R7 and the Evaluation Criteria in `README.md`), is that **lead time must be measured empirically against held-out historical events**, not asserted from a model's internal confidence — many published forecasting claims are weakened precisely because this distinction is blurred.

---

## Sequence Modeling Literature Behind Phase 4

The specific deep architectures named in `07_Tech_Stack.md` and `28_Transformer_Models.md` are drawn from established time-series forecasting literature, not solar-physics-specific research — HeliosAI applies general-purpose long-sequence forecasting advances to this domain:

- **LSTM/GRU** — the long-standing recurrent baseline for sequence modeling, still a reasonable mid-tier benchmark between classical ML and full Transformer architectures.
- **Informer** — introduced an efficient self-attention mechanism (ProbSparse attention) specifically to make Transformer-based forecasting tractable over long input sequences, relevant given HeliosAI's rolling precursor-window design.
- **PatchTST** — patches the input series into sub-sequences before attention, improving long-horizon forecasting efficiency and accuracy relative to point-wise attention, a natural fit for the rolling-window feature construction already scoped in `08_Development_Roadmap.md`.
- **Temporal Fusion Transformer (TFT)** — combines recurrent and attention components with built-in interpretability (variable selection networks, attention weight outputs), which aligns directly with HeliosAI's requirement that forecasts be explainable, not just accurate.

These architectures are treated as **candidates to be empirically compared** against the classical baseline (per Phase 4 in `08`), not assumed superior in advance.

---

## Explainable AI Literature Behind the XAI Layer

- **SHAP (SHapley Additive exPlanations)** — a game-theoretic feature-attribution method well suited to tree-based models (XGBoost/LightGBM/CatBoost), used for HeliosAI's classical-ML and nowcasting explainability.
- **Captum (integrated gradients, attention-weight visualization)** — PyTorch's explainability library, appropriate for the deep sequence models in Phase 4, allowing scientists to inspect which time steps and features drove a given forecast trigger.

The design principle stated in `08_Development_Roadmap.md` — explainability built **alongside** each model class, not retrofitted — reflects a recurring critique in applied ML-for-science literature: post-hoc explainability bolted onto an already-deployed model is less trustworthy and less actionable for domain experts than explainability designed in from the start.

---

## Gaps HeliosAI Aims to Address

Relative to prior single-instrument or single-band flare detection/forecasting systems, HeliosAI's literature-informed contributions are:

1. **Genuine dual-band (soft + hard X-ray) fusion** at the detection-confidence level, not just as two separately-reported outputs.
2. **Empirically measured, per-event lead time** as a first-class logged metric (MLflow), rather than a claimed model property.
3. **Explainability co-developed with both the nowcasting and forecasting tracks**, covering both tree-based and deep-sequence model families.
4. **A fully open, Python-native, reproducible reference implementation** — many space-weather forecasting efforts in the literature are not accompanied by openly runnable pipelines, which limits independent verification.

---

## Revision History

| Version | Date | Author | Notes |
|---|---|---|---|
| 0.1 | 2026-07-12 | HeliosAI Documentation (Antigravity workflow) | Initial Research Background — flare physics, classification, prior art in detection/forecasting, sequence-model and XAI literature, and identified gaps established |
