# HeliosAI
AI-Powered Space Weather Intelligence Platform Forecasting and Nowcasting of Solar Flares using Combined Soft X-ray (SoLEXS) and Hard X-ray (HEL1OS) Data from ISRO's Aditya-L1 Mission

## Running the Application

1. **Start Live Data Ingestion (Mock)**
   ```bash
   python scripts/live_data_poller.py
   ```

2. **Start the Dashboard**
   ```bash
   streamlit run app.py
   ```

Alternatively, you can run the application using Docker Compose:
```bash
docker-compose up --build
```
