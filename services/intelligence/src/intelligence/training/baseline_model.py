import mlflow
import pandas as pd
from typing import Tuple

# Placeholder for actual library imports like xgboost or lightgbm
# import xgboost as xgb 

class BaselineTrainer:
    """
    Implements the classical ML baseline training pipeline (Doc 26).
    Evaluates XGBoost, LightGBM, CatBoost on flattened feature vectors.
    """
    def __init__(self, experiment_name: str = "heliosai-flare-forecast-baseline"):
        self.experiment_name = experiment_name
        mlflow.set_experiment(experiment_name)

    def prepare_data(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
        """
        Flatten the feature inputs. Assume df contains targets.
        """
        # Time-based splitting logic goes here to avoid future leak
        pass

    def train_xgboost(self, X_train: pd.DataFrame, y_train: pd.Series):
        """
        Trains XGBoost baseline. Integrates SMOTE or class weighting
        to handle minority class (high-class flares).
        """
        with mlflow.start_run(run_name="xgboost_baseline"):
            mlflow.log_param("model_type", "xgboost")
            mlflow.log_param("imbalance_strategy", "class_weight")
            # model = xgb.XGBClassifier(scale_pos_weight=...)
            # model.fit(X_train, y_train)
            # mlflow.xgboost.log_model(model, "model")
            pass

    def train_lightgbm(self, X_train: pd.DataFrame, y_train: pd.Series):
        """
        Trains LightGBM baseline. 
        """
        with mlflow.start_run(run_name="lightgbm_baseline"):
            mlflow.log_param("model_type", "lightgbm")
            # model = lgb.LGBMClassifier(class_weight='balanced')
            # model.fit(X_train, y_train)
            # mlflow.lightgbm.log_model(model, "model")
            pass
