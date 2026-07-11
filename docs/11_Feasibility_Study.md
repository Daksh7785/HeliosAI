# 11 — Feasibility Study

**HeliosAI** — AI-Powered Space Weather Intelligence Platform
Document 11 of 61

---

## 1. Executive Summary

This document evaluates the technical and operational feasibility of HeliosAI within the context of the ISRO PS-15 Hackathon. It concludes that the proposed dual-band fusion approach is highly feasible given the available technologies, provided the data ingestion and synchronization hurdles are cleared early in the project timeline.

---

## 2. Purpose

To justify the chosen architecture and technology stack against alternative approaches, ensuring the team is not attempting a statistically or computationally impossible task.

---

## 3. Scope

Covers technical, data, and time feasibility.

---

## 4. Technical Feasibility

### 4.1 Compute Requirements
- **Constraint:** Training ML models (especially LSTMs) requires significant compute.
- **Feasibility:** High. While training deep models locally may be slow, the initial MVP uses XGBoost (`07_Tech_Stack.md`), which trains efficiently on CPU. Model inference (nowcasting/forecasting) is computationally cheap and easily runs within a standard Docker container.

### 4.2 Storage Requirements
- **Constraint:** Continuous time-series data can grow rapidly.
- **Feasibility:** High. TimescaleDB is specifically designed for this workload. For a single mission's light curves, standard SSD storage on a modern laptop or small cloud instance is more than sufficient for years of data.

---

## 5. Data Feasibility

### 5.1 Data Availability
- **Constraint:** The models require sufficient historical flare events for training.
- **Feasibility:** Medium-High. The ISSDC PRADAN portal provides Aditya-L1 data. If the mission's active period has not captured enough X/M-class flares, transfer learning from GOES data (simulating SoLEXS bands) may be required as a fallback strategy.

### 5.2 Data Quality
- **Constraint:** Telemetry may have gaps.
- **Feasibility:** High. The Processing subsystem (`03_System_Architecture.md`) is designed explicitly to handle this via interpolation and quarantine flagging, rather than assuming perfect data.

---

## 6. Algorithmic Feasibility

### 6.1 Dual-Band Fusion
- **Constraint:** Fusing soft and hard X-rays meaningfully to reduce False Alarm Rate (FAR).
- **Feasibility:** High. Scientific literature (`12_Research_Background.md`) supports the Neupert effect, indicating a strong correlation between the derivative of soft X-rays and the intensity of hard X-rays during flares. Our feature engineering (FR-PROC-03) leverages this physical reality, making algorithmic fusion highly viable compared to a purely black-box approach.

---

## 7. Interfaces to Other Documents

- **`07_Tech_Stack.md`** — The tools evaluated for technical feasibility.
- **`12_Research_Background.md`** — The scientific basis validating algorithmic feasibility.

---

## 8. Acceptance Criteria

- [ ] Evaluates compute, storage, data, and algorithmic constraints.
- [ ] Provides a clear "Feasible" / "Not Feasible" / "Requires Fallback" rating for each.

---

## 9. Review Checklist

- [ ] Does not assume perfect data availability.

---

## 10. Future Improvements

- Re-evaluate compute feasibility if transitioning to massive ensemble models.

---

## Antigravity Development Prompt

```
PROJECT CONTEXT:
HeliosAI dual-band Aditya-L1 flare nowcasting/forecasting platform (ISRO PS-15).
Document 11 of 61: Feasibility Study.

FOLDER: docs/11_Feasibility_Study.md

FILES TO PRODUCE: docs/11_Feasibility_Study.md only.

CODING STANDARDS: Markdown. Follow the shared template.

EXPECTED OUTPUT: Feasibility analysis across technical, data, and algorithmic domains.

EDGE CASES / VALIDATION: None.

TESTING: Markdown lint.

ACCEPTANCE CRITERIA: See §8 above.

DELIVERABLES: docs/11_Feasibility_Study.md

GIT COMMIT FORMAT: docs: add 11_Feasibility_Study.md (feasibility analysis)
```

---

**Next document:** `12_Research_Background.md` — say **NEXT** to continue.
