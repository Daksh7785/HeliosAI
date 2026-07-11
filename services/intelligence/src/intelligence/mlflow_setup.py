import mlflow
from shared.config.settings import settings
import logging

logger = logging.getLogger(__name__)

def setup_mlflow():
    """Configure MLflow tracking URI."""
    try:
        mlflow.set_tracking_uri(settings.MLFLOW_TRACKING_URI)
        mlflow.set_experiment("heliosai-flare-forecast")
        logger.info(f"MLflow tracking URI set to {settings.MLFLOW_TRACKING_URI}")
    except Exception as e:
        logger.error(f"Failed to set MLflow tracking URI: {e}")
        
def load_production_model(model_name: str = "flare_predictor"):
    """Load the latest production model from MLflow registry."""
    model_uri = f"models:/{model_name}/Production"
    try:
        return mlflow.pyfunc.load_model(model_uri)
    except Exception as e:
        logger.warning(f"Could not load model {model_name} from MLflow: {e}")
        return None
