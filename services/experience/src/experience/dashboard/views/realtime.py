import streamlit as st
import requests
import pandas as pd
import time

API_BASE_URL = "http://localhost:8000/api/v1"

def fetch_forecasts():
    try:
        # Placeholder for actual API call
        # response = requests.get(f"{API_BASE_URL}/forecasts")
        # return response.json().get("forecasts", [])
        return [{"horizon": "1h", "probability_x_class": 0.15, "probability_m_class": 0.45}]
    except Exception:
        return []

def render_realtime():
    st.header("Real-time Monitor")
    st.write("Live forecast predictions based on continuous ingestion.")
    
    forecasts = fetch_forecasts()
    
    if not forecasts:
        st.warning("Unable to reach the Serving API or no active forecasts available.")
        return

    st.subheader("Current Predictive Probabilities")
    
    col1, col2, col3 = st.columns(3)
    
    # Mock rendering based on the first horizon
    latest = forecasts[0]
    
    with col1:
        st.metric(label="X-Class Flare Probability (Next 1h)", value=f"{latest['probability_x_class']*100:.1f}%")
    with col2:
        st.metric(label="M-Class Flare Probability (Next 1h)", value=f"{latest['probability_m_class']*100:.1f}%")
        
    st.write("*(Note: To enable true WebSockets streaming, run the FastAPI backend with Redis/PubSub and adapt this view to use `st_websocket` or a cyclic `st.rerun()` pattern.)*")
    
    if st.button("Refresh Manually"):
        st.rerun()
