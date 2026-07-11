# 28 — Transformer Models

> **Document 28 of 61** in the HeliosAI documentation set (see `README.md` → Repository Structure). Details the advanced attention-based models used in the Forecasting Engine.

---

## Table of Contents

1. [Purpose of This Document](#purpose-of-this-document)
2. [Why Transformers for Time Series?](#why-transformers-for-time-series)
3. [Implemented Architectures](#implemented-architectures)
4. [Explainability via Attention](#explainability-via-attention)

---

## Purpose of This Document

This document covers the most advanced modeling tier in HeliosAI: Transformer-based time-series forecasting.

## Why Transformers for Time Series?

LSTMs and GRUs (`27_Deep_Learning.md`) can struggle with very long context windows. Transformers, using self-attention, can weigh the importance of a hard X-ray precursor spike 45 minutes ago against a soft X-ray flux gradient happening *right now*, without the vanishing gradient problems of RNNs.

## Implemented Architectures

1. **Temporal Fusion Transformer (TFT):** Highly interpretable; supports static metadata (e.g., known solar cycle phase) alongside dynamic time-series data.
2. **Informer / PatchTST:** Optimized for long-sequence time-series forecasting. By "patching" the time series into overlapping segments, PatchTST significantly reduces memory overhead while preserving local temporal structure.

## Explainability via Attention

Transformers naturally align with HeliosAI's explainability mandate (`29_Explainable_AI.md`). Attention weights are directly extracted during inference to show operators *which* historical segment of the light curve contributed most heavily to the current forecast probability.

**Next document:** `29_Explainable_AI.md`
