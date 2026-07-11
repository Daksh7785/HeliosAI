class HeliosException(Exception):
    """Base exception for all HeliosAI custom errors."""
    def __init__(self, message: str, code: str = "HELIOS_ERROR"):
        self.message = message
        self.code = code
        super().__init__(self.message)

class IngestionError(HeliosException):
    """Raised when ingestion encounters unparseable or malformed data."""
    def __init__(self, message: str):
        super().__init__(message, code="INGESTION_ERROR")

class ProcessingError(HeliosException):
    """Raised during feature engineering or filtering failures."""
    def __init__(self, message: str):
        super().__init__(message, code="PROCESSING_ERROR")

class ModelInferenceError(HeliosException):
    """Raised when a model fails to generate a prediction or nowcast."""
    def __init__(self, message: str):
        super().__init__(message, code="INFERENCE_ERROR")

class ConfigurationError(HeliosException):
    """Raised when the environment is incorrectly configured."""
    def __init__(self, message: str):
        super().__init__(message, code="CONFIG_ERROR")
