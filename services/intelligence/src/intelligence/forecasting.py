import pandas as pd
from typing import Dict, Any, List
import logging
from datetime import datetime

from intelligence.mlflow_setup import load_production_model

logger = logging.getLogger(__name__)

class Forecaster:
    """
    Implements the Forecasting Engine:
    Predicts the probability of a flare occurring within N minutes
    (15/30/60) using a loaded MLflow model.
    """
    def __init__(self, model_name: str = "flare_forecaster_baseline"):
        self.model_name = model_name
        self.model = load_production_model(model_name)
        if self.model is None:
            logger.warning(f"No production model found for '{model_name}'. Using mock fallback.")

    def _calibrate_probabilities(self, raw_probs: List[float], flare_class: str) -> List[float]:
        """
        Calibrate raw probabilities per class (e.g. Platt scaling / isotonic regression).
        Placeholder for isotonic regression implementation.
        """
        return [min(1.0, max(0.0, p)) for p in raw_probs]

    def _compute_lead_time(self, predicted_trigger_ts: datetime, actual_peak_ts: datetime) -> float:
        """
        Computes lead time in minutes if a ground truth event occurs.
        """
        return (actual_peak_ts - predicted_trigger_ts).total_seconds() / 60.0

    def predict(self, features_df: pd.DataFrame, horizons_min: List[int] = [15, 30, 60]) -> Dict[str, Any]:
        """
        Given a lookback window of features, predict probabilities for the future horizons.
        """
        if features_df.empty:
            return {"error": "Empty feature dataframe provided"}

        results = {}
        for horizon in horizons_min:
            if self.model:
                try:
                    # In a real model, horizon might be a feature or we might use specific models per horizon
                    raw_pred = self.model.predict(features_df)
                    # mock processing raw_pred array
                    prob = float(raw_pred[0]) if hasattr(raw_pred, '__getitem__') else 0.5
                    flare_class = "M" if prob > 0.8 else "C"
                except Exception as e:
                    logger.error(f"Inference failed: {e}")
                    prob, flare_class = 0.0, "Unknown"
            else:
                # Mock fallback
                prob = 0.15 * (60 / horizon) # naive rule
                flare_class = "C"

            # Calibrate (mocked)
            calibrated_probs = self._calibrate_probabilities([prob], flare_class)
            final_prob = calibrated_probs[0]

            results[f"horizon_{horizon}m"] = {
                "probability": final_prob,
                "class": flare_class,
                "model_version": f"{self.model_name}_prod"
            }

        return {
            "forecasts": results,
            "timestamp_processed": datetime.utcnow()
        }
