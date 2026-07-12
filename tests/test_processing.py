import pytest
import numpy as np
import pandas as pd
import os
import tempfile
from src.data_loader import generate_simulated_data, load_and_merge_data

def test_generate_simulated_data():
    with tempfile.TemporaryDirectory() as tmpdir:
        solexs_path, helios_path = generate_simulated_data(output_dir=tmpdir, duration_hours=1)
        assert os.path.exists(solexs_path)
        assert os.path.exists(helios_path)
        
        df_solexs = pd.read_csv(solexs_path)
        assert len(df_solexs) == 3600
        
def test_data_quality_flags():
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create dummy data with negative flux
        solexs_path = os.path.join(tmpdir, "solexs.csv")
        helios_path = os.path.join(tmpdir, "helios.csv")
        
        pd.DataFrame({
            'timestamp': ['2024-01-01 00:00:00', '2024-01-01 00:00:01'],
            'solexs_flux': [1e-7, -1e-7]
        }).to_csv(solexs_path, index=False)
        
        pd.DataFrame({
            'timestamp': ['2024-01-01 00:00:00', '2024-01-01 00:00:01'],
            'helios_flux': [1e-8, 1e-8]
        }).to_csv(helios_path, index=False)
        
        df_merged = load_and_merge_data(solexs_path, helios_path)
        
        # Check that the first row is VALIDATED and second is QUARANTINED
        assert df_merged.loc[0, 'data_quality_flag'] == 'VALIDATED'
        assert df_merged.loc[1, 'data_quality_flag'] == 'QUARANTINED'
        
        # Check imputation (forward fill from row 0)
        assert df_merged.loc[1, 'solexs_flux'] == 1e-7
