# 59 — Research Paper

**HeliosAI** — AI-Powered Space Weather Intelligence Platform
Document 59 of 61

---

## 1. Purpose

Outlines the structure and content plan for a scientific writeup of HeliosAI's methodology and results, intended for submission to a space-weather or applied-ML venue, and/or as supporting documentation for the Problem Statement 15 evaluation.

---

## 2. Proposed Paper Structure

| Section | Content |
|---|---|
| **1. Abstract** | Summary of dual-band (SoLEXS + HEL1OS) fusion approach, headline TPR/FAR and lead-time results |
| **2. Introduction** | Space weather impact motivation, Aditya-L1 mission context, gap this work addresses (single-band vs. dual-band detection) |
| **3. Related Work** | Prior solar flare detection/forecasting literature (GOES-based, other spacecraft), positioning HeliosAI's cross-band fusion contribution |
| **4. Data** | SoLEXS/HEL1OS Level-1 data description, time range covered, preprocessing summary (references `18_Data_Preprocessing.md`, `19_Data_Synchronization.md`) |
| **5. Methods** | Nowcasting algorithm (per-band detection + fusion), forecasting models (baseline + deep sequence models), feature engineering (`21_Feature_Engineering.md`) |
| **6. Experimental Setup** | Train/val/test time-forward split methodology, evaluation metrics (`48_Model_Evaluation.md`) |
| **7. Results** | Per-class TPR/FAR tables, lead-time distributions, calibration curves, ablation (dual-band vs. single-band-only baseline) |
| **8. Explainability** | SHAP/attention-based case studies of representative detected/forecast events (`29_Explainable_AI.md`) |
| **9. Discussion** | Where the model succeeds/fails (e.g., performance on rare X-class events), physical interpretation of learned precursor patterns |
| **10. Limitations** | Data volume constraints, non-certified research-only status, small high-class sample sizes |
| **11. Future Work** | Multi-mission fusion, magnetogram integration (`60_Future_Enhancements.md`) |
| **12. Conclusion** | Restated contribution and quantified headline results |

---

## 3. Reproducibility Package

Alongside the paper, the following are released for reproducibility:
- Pinned environment specification (matching `47_Model_Training.md`'s logged environment).
- MLflow experiment export for the reported model version.
- Evaluation notebook reproducing all reported tables/figures from the Analytics marts (`43_Analytics.md`).

---

## 4. Key Claims Requiring Empirical Backing (Not Asserted)

Per the project's stated design principle of measuring rather than asserting performance, the paper will report (not presuppose):
- Actual measured lead-time distribution (median, IQR) — not a target number.
- Actual measured dual-band vs. single-band FAR reduction — quantified via ablation, per README's stated differentiator claim.
- Actual per-class TPR, with confidence intervals for low-sample-size classes.

---

## 5. Authorship & Attribution

Draft author list and contribution statement to be finalized once implementation and evaluation phases conclude; this document reserves the structural placeholder only.

---

## 6. Interfaces to Other Documents

- **`48_Model_Evaluation.md`** — source of all quantitative results reported.
- **`29_Explainable_AI.md`** — source of case-study material.
- **`43_Analytics.md`** — source of figures/tables.
- **`60_Future_Enhancements.md`** — feeds the paper's Future Work section.

---

**Next document:** `60_Future_Enhancements.md` — say **NEXT** to continue.
