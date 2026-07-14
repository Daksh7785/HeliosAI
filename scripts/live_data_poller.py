import time
import pandas as pd
import numpy as np
import os
import datetime

# Mock live data ingestion for Aditya-L1 SUIT/SoLEXS/HELIOS payloads
DATA_DIR = os.path.join(os.path.dirname(__file__), '../data')
os.makedirs(DATA_DIR, exist_ok=True)

LIVE_CSV_PATH = os.path.join(DATA_DIR, 'live_solar_flux.csv')

def fetch_live_data():
    """Mock fetching data from ISRO Aditya-L1 API"""
    now = datetime.datetime.now()
    
    # Generate some random fluctuations
    solexs_flux = max(0, np.random.normal(1e-7, 1e-8))
    helios_flux = max(0, np.random.normal(1e-8, 1e-9))
    
    # Occasional flare simulation
    if np.random.rand() > 0.95:
        solexs_flux *= 100
        helios_flux *= 100
        
    return {
        'timestamp': now.isoformat(),
        'solexs_flux': solexs_flux,
        'helios_flux': helios_flux
    }

def main():
    print(f"Starting live data ingestion. Writing to {LIVE_CSV_PATH}...")
    
    # Create header if file doesn't exist
    if not os.path.exists(LIVE_CSV_PATH):
        df = pd.DataFrame(columns=['timestamp', 'solexs_flux', 'helios_flux'])
        df.to_csv(LIVE_CSV_PATH, index=False)
        
    while True:
        try:
            data = fetch_live_data()
            df = pd.DataFrame([data])
            df.to_csv(LIVE_CSV_PATH, mode='a', header=False, index=False)
            print(f"Ingested data at {data['timestamp']} | SoLEXS: {data['solexs_flux']:.2e} | HELIOS: {data['helios_flux']:.2e}")
            time.sleep(5)  # Poll every 5 seconds
        except KeyboardInterrupt:
            print("Stopping live ingestion...")
            break
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()
