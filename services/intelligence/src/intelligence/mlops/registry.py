import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)

class ModelRegistry:
    """
    Model Registry (Doc 45)
    Tracks versions, promotes models, and serves current production models.
    """
    def __init__(self):
        self._registry = {}
        
    def register_model(self, name: str, version: str, artifact_path: str):
        logger.info(f"Registering model {name} v{version}")
        if name not in self._registry:
            self._registry[name] = {}
        self._registry[name][version] = {
            "artifact_path": artifact_path,
            "status": "Staging"
        }
        
    def promote_to_production(self, name: str, version: str):
        logger.info(f"Promoting {name} v{version} to Production")
        for v in self._registry.get(name, {}).values():
            if v["status"] == "Production":
                v["status"] = "Archived"
        self._registry[name][version]["status"] = "Production"
        
    def get_production_model(self, name: str) -> Dict[str, Any]:
        models = self._registry.get(name, {})
        for version, details in models.items():
            if details["status"] == "Production":
                return {"version": version, "details": details}
        return None
