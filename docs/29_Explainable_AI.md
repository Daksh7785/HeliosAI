# 29 — Explainable AI (XAI)

> **Document 29 of 61** in the HeliosAI documentation set (see `README.md` → Repository Structure). Details how HeliosAI models remain transparent and interpretable.

---

## Table of Contents

1. [Purpose of This Document](#purpose-of-this-document)
2. [The Interpretability Mandate](#the-interpretability-mandate)
3. [Tree-Based Explainability (SHAP)](#tree-based-explainability-shap)
4. [Deep Learning Explainability (Captum)](#deep-learning-explainability-captum)
5. [Serving Explanations](#serving-explanations)

---

## Purpose of This Document

This document defines how predictions made by the Forecasting Engine (`23_Forecasting.md`) are explained to human operators, transforming "black box" models into trusted operational tools.

## The Interpretability Mandate

In space weather operations, a high-probability warning for an X-class flare is only actionable if researchers understand *why* the warning was issued. Is it due to a sudden HEL1OS spike, or a steady climb in SoLEXS background flux?

## Tree-Based Explainability (SHAP)

For baseline models (XGBoost, LightGBM, CatBoost):
- **Tool:** SHAP (SHapley Additive exPlanations) TreeExplainer.
- **Output:** Feature importance rankings and dependence plots.
- **Integration:** SHAP values are calculated asynchronously via Celery (`34_Background_Jobs.md`) after each major forecast generation.

## Deep Learning Explainability (Captum)

For deep sequence and Transformer models:
- **Tool:** PyTorch Captum.
- **Methods:** Integrated Gradients (for LSTMs/GRUs) and Attention Rollout (for Transformers).
- **Output:** A temporal heatmap overlaid on the light curve, highlighting the exact timestamps and features that drove the prediction.

## Serving Explanations

Explanation artifacts are serialized, stored in the database (`30_Database_Design.md`), and served via dedicated REST endpoints (`32_API_Design.md`) to the Dashboard's Explainability View.

**Next document:** `30_Database_Design.md`
