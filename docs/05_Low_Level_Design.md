# 05 — Low-Level Design (LLD)

**HeliosAI** — AI-Powered Space Weather Intelligence Platform
Document 05 of 61

---

## 1. Purpose

This document provides class-level and interface-level detail for the core HeliosAI components. It serves as the direct blueprint for software engineers implementing the system described in `04_High_Level_Design.md`.

---

## 2. Core Interfaces

### 2.1 The BaseModelPredictor Interface
Every forecasting and nowcasting model must conform to this abstract base class. This ensures the Intelligence Layer can swap models without refactoring the calling code.

```python
from abc import ABC, abstractmethod
from typing import Dict, Any
import pandas as pd

class BaseModelPredictor(ABC):
    @abstractmethod
    def load_model(self, model_uri: str) -> None:
        """Loads model weights/artifacts from MLflow or local cache."""
        pass

    @abstractmethod
    def predict_proba(self, features: pd.DataFrame) -> Dict[str, float]:
        """
        Returns probability distribution across flare classes.
        Example: {'B': 0.8, 'C': 0.15, 'M': 0.04, 'X': 0.01}
        """
        pass

    @abstractmethod
    def explain(self, features: pd.DataFrame) -> Dict[str, Any]:
        """
        Returns feature importance or SHAP values for the given prediction.
        """
        pass
```

### 2.2 The Data Fetcher Interface
Standardizes ingestion across different ISRO API endpoints.

```python
from abc import ABC, abstractmethod
from datetime import datetime
import pandas as pd

class BaseTelemetryFetcher(ABC):
    @abstractmethod
    def fetch_window(self, start: datetime, end: datetime) -> pd.DataFrame:
        """Fetches telemetry for the specified time window."""
        pass
```

---

## 3. Database Repositories

Using the Repository pattern to encapsulate SQLAlchemy operations.

### 3.1 FeatureRepository
```python
class FeatureRepository:
    def save_features(self, df: pd.DataFrame) -> str:
        """Saves a batch of features and returns a snapshot_id."""
        pass

    def get_features(self, start: datetime, end: datetime) -> pd.DataFrame:
        """Retrieves synchronized features for a time window."""
        pass
```

### 3.2 CatalogueRepository
```python
class CatalogueRepository:
    def add_tentative_event(self, event_data: dict) -> int:
        """Logs a single-band detection."""
        pass

    def promote_to_confirmed(self, event_id: int, cross_band_data: dict) -> None:
        """Upgrades a tentative event to confirmed upon dual-band fusion."""
        pass
```

---

## 4. Celery Task Definitions

The asynchronous pipeline relies on specific task signatures.

### 4.1 Ingestion Tasks
- `fetch_solexs_data(start_iso: str, end_iso: str) -> bool`
- `fetch_hel1os_data(start_iso: str, end_iso: str) -> bool`

### 4.2 Processing Tasks
- `sync_and_engineer_features(window_start: str, window_end: str) -> str` (Returns `snapshot_id`)

### 4.3 Intelligence Tasks
- `run_nowcast_inference(snapshot_id: str) -> dict`
- `run_forecast_inference(snapshot_id: str) -> dict`

---

## 5. Dependency Injection

To facilitate testing, core services receive their dependencies (repositories, predictors) via constructor injection.

```python
class ForecastingService:
    def __init__(self, predictor: BaseModelPredictor, repo: FeatureRepository):
        self.predictor = predictor
        self.repo = repo

    def execute_forecast(self, start: datetime, end: datetime):
        features = self.repo.get_features(start, end)
        probabilities = self.predictor.predict_proba(features)
        # ... logic to save results and trigger alerts ...
```

---

## 6. Interfaces to Other Documents

- **`04_High_Level_Design.md`** — provides the context for these classes.
- **`56_Coding_Standards.md`** — dictates the exact typing and documentation requirements for these signatures.

---

## 7. Acceptance Criteria

- [ ] All critical ML and data-access interfaces are defined.
- [ ] Dependency injection is explicitly modeled.
- [ ] Celery task boundaries reflect the HLD pipeline.

---

## 8. Review Checklist

- [ ] Ensure Python typings are modern (e.g., `Dict`, `Any`, `pd.DataFrame`).
- [ ] Confirm the `BaseModelPredictor` supports both probabilities and explainability.

---

## 9. Future Improvements

- Add concrete interface definitions for the Alert Dispatcher once the external notification providers (e.g., SendGrid, Slack) are selected.

---

## Antigravity Development Prompt

```
PROJECT CONTEXT:
You are implementing a documentation-only artifact — this task produces no source code.
Repository: HeliosAI. This is document 05 of a 61-document specification set.

FOLDER:
docs/05_Low_Level_Design.md

FILES TO PRODUCE:
None (documentation task). Output exactly one file: docs/05_Low_Level_Design.md

CODING STANDARDS:
N/A — Markdown only. Follow the structural template used by all other docs.

EXPECTED OUTPUT:
A single self-contained Markdown file outlining class interfaces, repositories, and task signatures.

TESTING:
Documentation-only — validation is a Markdown lint pass.

ACCEPTANCE CRITERIA:
See §7 above.

DELIVERABLES:
docs/05_Low_Level_Design.md

GIT COMMIT FORMAT:
docs: add 05_Low_Level_Design.md (class diagrams and interfaces)
```

---

**Next document:** `06_Project_Folder_Structure.md` — say **NEXT** to continue.
