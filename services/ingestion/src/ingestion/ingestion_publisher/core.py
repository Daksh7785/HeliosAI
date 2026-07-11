import json
from typing import Dict, Any
from structlog import get_logger
from .interface import PublisherProtocol

logger = get_logger(__name__)

class RedisPublisher(PublisherProtocol):
    """Publishes validated data to a Redis queue for processing."""
    def __init__(self, redis_url: str, queue_name: str = "raw_light_curves"):
        self.redis_url = redis_url
        self.queue_name = queue_name
        
    def publish(self, valid_data: Dict[str, Any]) -> None:
        import redis
        
        logger.info("publishing_data", file_name=valid_data.get("file_name"), queue=self.queue_name)
        try:
            # We connect per publish or keep a connection pool in production
            client = redis.from_url(self.redis_url)
            payload = json.dumps(valid_data)
            client.lpush(self.queue_name, payload)
        except Exception as e:
            logger.error("publish_failed", error=str(e), file=valid_data.get("file_name"))
            raise
