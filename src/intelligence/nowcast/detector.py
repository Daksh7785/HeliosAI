import pandas as pd
from src.intelligence.base_model import BaseModelPredictor

class ThresholdDetector(BaseModelPredictor):
    """
    Baseline nowcasting engine based on static hardness ratio thresholds.
    """
    def __init__(self, hardness_threshold=0.5, consecutive_points=3):
        self.hardness_threshold = hardness_threshold
        self.consecutive_points = consecutive_points
        
    def load_model(self, path: str):
        pass # No dynamic weights for baseline
        
    def save_model(self, path: str):
        pass

    def predict(self, feature_df: pd.DataFrame) -> pd.DataFrame:
        """
        Detects flare events in a timeseries DataFrame of features.
        Expects columns: timestamp, solexs_flux, hel1os_flux, hardness_ratio
        Returns a DataFrame of detected flare events.
        """
        if feature_df.empty:
            return pd.DataFrame()
            
        df = feature_df.copy()
        df = df.sort_values('timestamp')
        
        # Boolean mask for above threshold
        df['above_thresh'] = df['hardness_ratio'] > self.hardness_threshold
        
        # Find consecutive sequences
        # This is a simple rolling window sum to find when we hit 'consecutive_points' triggers
        df['trigger'] = df['above_thresh'].rolling(window=self.consecutive_points).sum() >= self.consecutive_points
        
        events = []
        in_flare = False
        start_time = None
        peak_time = None
        peak_flux = 0
        
        for _, row in df.iterrows():
            if row['trigger'] and not in_flare:
                # Flare starts
                in_flare = True
                start_time = row['timestamp']
                peak_time = start_time
                peak_flux = row['solexs_flux']
            elif in_flare:
                # Update peak if we are higher
                if row['solexs_flux'] > peak_flux:
                    peak_flux = row['solexs_flux']
                    peak_time = row['timestamp']
                    
                # End flare if we drop below threshold
                if not row['above_thresh']:
                    in_flare = False
                    end_time = row['timestamp']
                    
                    # Approximate GOES class based on SoLEXS peak flux mapping (mock logic)
                    # A true implementation would use the conversion formula
                    flare_class = "C" if peak_flux < 100 else ("M" if peak_flux < 500 else "X")
                    
                    events.append({
                        'start_time': start_time,
                        'peak_time': peak_time,
                        'end_time': end_time,
                        'class_level': f"{flare_class}-class (mock)",
                        'peak_flux': peak_flux,
                        'source': 'HeliosAI-Nowcast-Baseline'
                    })
                    
        # If still in flare at the end of the data, close it
        if in_flare:
            events.append({
                'start_time': start_time,
                'peak_time': peak_time,
                'end_time': df.iloc[-1]['timestamp'],
                'class_level': "Unknown",
                'peak_flux': peak_flux,
                'source': 'HeliosAI-Nowcast-Baseline'
            })
            
        return pd.DataFrame(events)
