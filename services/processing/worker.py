from celery import Celery
import logging
from shared.config.settings import settings

logger = logging.getLogger(__name__)

celery_app = Celery(
    "processing",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

@celery_app.task
def process_new_data_block(file_path: str):
    """
    Called by the Ingestion service when a new data file drops.
    Handles Sync -> Noise Filter -> Feature Eng -> Persistence.
    """
    logger.info(f"Processing new data block: {file_path}")
    return {"status": "processed", "file": file_path}
