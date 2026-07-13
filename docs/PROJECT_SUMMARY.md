# HeliosAI: Solar Flare Nowcasting & Forecasting Solution

This document provides a complete summary of the features and modules built for the Aditya-L1 Solar Flare Hackathon challenge. The solution is fully working and strictly aligns with all expected outcomes and evaluation criteria.

---

## 1. System Overview
HeliosAI is a complete intelligence pipeline that ingests Soft X-ray (SoLEXS) and Hard X-ray (HEL1OS) data from ISRO's Aditya-L1 mission, identifies active solar flares in real-time (Nowcasting), and predicts upcoming flares before they peak (Forecasting) using Machine Learning.

The entire system is accessible via a unified, interactive **Streamlit Dashboard** (`app.py`).

---

## 2. Features Built & Objectives Addressed

### Objective 1: Data Ingestion & Preprocessing
*Hackathon Requirement: "Download SoLEXS and HEL1OS from ISSDC portal. Write scripts to read... time-series light curve data."*

**What we built:**
- **`src/data_loader.py`**: We implemented a robust FITS file parser using `astropy`. It automatically identifies the binary table extensions standard to ISRO Level-1 data and extracts Time and Flux arrays for both SoLEXS and HEL1OS payloads.
- **Data Toggling**: The dashboard includes a sidebar toggle to switch seamlessly between realistic Simulated Data (for immediate testing) and Real ISSDC Data.
- **ISSDC Guide**: We provided `src/ingestion/issdc_instructions.md`, detailing exactly how to navigate the PRADAN portal and where to place the downloaded data for the pipeline to automatically read it.

### Objective 2: Algorithmic Nowcasting (Real-Time Detection)
*Hackathon Requirement: "Build algorithms to detect flares independently in both soft and hard X-rays. Combine these... to generate a master catalogue."*

**What we built:**
- **`src/flare_detector.py`**: We developed an algorithmic nowcasting engine that applies a sliding-window Median Absolute Deviation (MAD) threshold. This dynamically adjusts to the background noise floor of the X-ray flux.
- **Independent Detection**: The algorithm detects spikes independently for Soft X-rays (gradual) and Hard X-rays (impulsive).
- **Master Catalogue Fusion**: Detections are fused into a "Master Flare Catalogue", automatically classifying the flare (C, M, X class) based on the peak flux magnitude. This catalogue is displayed directly on the dashboard.

### Objective 3: Predictive Modeling (Forecasting)
*Hackathon Requirement: "Train a time-series model using combined dataset to predict the probability of a flare occurring in the next N minutes."*

**What we built:**
- **`src/forecaster.py`**: We engineered time-series features (rolling mean, standard deviation, max, and derivative/rate-of-change over specific windows) for both soft and hard X-rays to capture precursor patterns (like the Neupert effect).
- **XGBoost Classifier**: We implemented an XGBoost model that predicts whether a flare will occur exactly within the next 15 minutes (`lead_time_minutes`).
- **Interactive Training**: You can click "Retrain Forecast Model" directly in the dashboard to retrain the model instantaneously whenever new ISSDC data is ingested.

### Objective 4: Visual Alerts & Interface
*Hackathon Requirement: "Interface that visualizes the X-ray light curves and triggers with visual alerts when a flare is nowcasted or forecasted."*

**What we built:**
- **Plotly Visualizations**: High-performance, synchronized, multi-row plots in the dashboard visualize the SoLEXS flux, HEL1OS flux, and the continuous Forecast Probability curve over time.
- **Dynamic Alert Banner**: We implemented an active alert banner at the top of the UI.
  - 🚨 **ACTIVE FLARE ALERT**: Triggers and turns red when the nowcast algorithm detects an ongoing flare.
  - ⚠️ **FORECAST ALERT**: Triggers and turns yellow when the predictive model outputs a >50% probability of an imminent flare.

### Objective 5: Evaluation Criteria
*Hackathon Requirement: "High True Positive Rate and low False Alarm Rate... Lead Time of predictions."*

**What we built:**
- **Metrics Engine**: The forecasting pipeline calculates specific confusion-matrix metrics during model training.
- **Evaluation Dashboard**: The dashboard sidebar displays the **True Positive Rate (TPR)**, **False Alarm Rate (FAR)**, and **Average Lead Time**, providing immediate, mathematical proof of the model's accuracy to the hackathon judges.

---

## 3. How to Run & Verify
1. Ensure dependencies are installed: `pip install -r requirements.txt`
2. Start the dashboard: `streamlit run app.py`
3. Click **"Retrain Forecast Model"** in the sidebar to generate the evaluation metrics.
4. Move the Time Range slider to visualize flares and observe the dynamic visual alerts triggering automatically.
