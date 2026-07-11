"""
Monitoring metrics for HeliosAI.
"""
from prometheus_fastapi_instrumentator import Instrumentator

def setup_monitoring(app):
    """
    Setup Prometheus instrumentation for a FastAPI app.
    """
    Instrumentator().instrument(app).expose(app)
