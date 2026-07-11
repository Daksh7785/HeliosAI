import pandas as pd
from typing import Dict, Any

from intelligence.mlflow_setup import load_production_model

class FlarePredictor:
    def __init__(self):
        self.model = load_production_model()
        
    def predict(self, features: pd.DataFrame) -> Dict[str, Any]:
        """
        Runs inference on the provided feature DataFrame.
        """
        if self.model is None:
            # Fallback mock prediction
            return {"probability": 0.1, "class": "M"}
            
        prediction = self.model.predict(features)
        
        # Format the output assuming the model returns a probability array or similar
        # This will need to be adapted based on the actual model format
        return {
            "probability": float(prediction[0]),
            "class": "X" if prediction[0] > 0.8 else "M"
        }
