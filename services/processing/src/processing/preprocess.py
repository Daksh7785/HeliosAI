import numpy as np
import logging

logger = logging.getLogger(__name__)

class Preprocessor:
    """
    Handles noise filtering and background subtraction (Doc 18).
    """
    def __init__(self, filter_window: int = 5, bg_window: int = 60):
        self.filter_window = filter_window
        self.bg_window = bg_window

    def median_filter(self, data: np.ndarray) -> np.ndarray:
        """
        Applies a moving median filter to remove high-frequency noise spikes.
        """
        if len(data) < self.filter_window:
            return data
            
        filtered = np.copy(data)
        for i in range(len(data)):
            start = max(0, i - self.filter_window // 2)
            end = min(len(data), i + self.filter_window // 2 + 1)
            filtered[i] = np.median(data[start:end])
        return filtered

    def subtract_background(self, data: np.ndarray) -> np.ndarray:
        """
        Subtracts a rolling minimum background to isolate flare signals.
        """
        if len(data) < self.bg_window:
            return data
            
        bg_subtracted = np.copy(data)
        for i in range(len(data)):
            start = max(0, i - self.bg_window)
            bg = np.min(data[start:i+1])
            bg_subtracted[i] = max(0, data[i] - bg)  # Ensure non-negative
        return bg_subtracted

    def process_series(self, data: np.ndarray) -> np.ndarray:
        """
        Executes the full preprocessing pipeline.
        """
        logger.debug("Applying median filter for noise reduction")
        filtered = self.median_filter(data)
        
        logger.debug("Applying background subtraction")
        processed = self.subtract_background(filtered)
        
        return processed
