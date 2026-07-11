# 27 — Deep Learning (Sequence Models)

> **Document 27 of 61** in the HeliosAI documentation set (see `README.md` → Repository Structure). Details the recurrent neural network models used in the Forecasting Engine.

---

## Table of Contents

1. [Purpose of This Document](#purpose-of-this-document)
2. [Recurrent Architectures](#recurrent-architectures)
3. [Input Representation](#input-representation)
4. [Training and Tuning](#training-and-tuning)

---

## Purpose of This Document

This document covers the implementation of RNN-based sequence models (LSTMs and GRUs) for predicting solar flares based on time-series inputs from SoLEXS and HEL1OS.

## Recurrent Architectures

While baseline models (`26_Machine_Learning.md`) use aggregated features, deep sequence models process the raw or smoothed chronological data directly:
- **LSTM (Long Short-Term Memory):** Captures extended dependencies, particularly the slow flux buildup leading to an event.
- **GRU (Gated Recurrent Unit):** A lighter, faster alternative to LSTM with comparable performance for high-frequency light curves.

## Input Representation

The models consume a 3D tensor: `(batch_size, sequence_length, num_features)`.
- `sequence_length` is determined by the feature window (e.g., 60 minutes of 1-second cadence data).
- `num_features` includes normalized SoLEXS flux, HEL1OS flux, their temporal derivatives, and spectral hardness.

## Training and Tuning

- **Loss Function:** Focal Loss or weighted Cross-Entropy to handle the extreme class imbalance (X-class flares are exceedingly rare compared to A/B/C flares).
- **Optimization:** AdamW with a learning rate scheduler (e.g., Cosine Annealing with Warm Restarts).
- **Early Stopping:** Monitored against validation Brier score.

**Next document:** `28_Transformer_Models.md`
