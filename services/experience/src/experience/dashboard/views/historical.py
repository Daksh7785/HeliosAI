import streamlit as st
import requests
import pandas as pd

API_BASE_URL = "http://localhost:8000/api/v1"

def fetch_catalogue(limit=100):
    try:
        # Placeholder for actual API call
        # response = requests.get(f"{API_BASE_URL}/catalogue?limit={limit}")
        # return response.json().get("events", [])
        return [
            {"event_id": "FL-20260712-001", "timestamp": "2026-07-12T00:15:00Z", "class": "M2.4", "confidence": 0.98},
            {"event_id": "FL-20260711-002", "timestamp": "2026-07-11T14:22:00Z", "class": "C5.1", "confidence": 0.95}
        ]
    except Exception:
        return []

def render_historical():
    st.header("Historical Catalogue")
    st.write("Review past flare events detected and classified by the intelligence pipeline.")
    
    limit = st.slider("Number of records to fetch", min_value=10, max_value=500, value=100)
    
    events = fetch_catalogue(limit=limit)
    
    if not events:
        st.warning("No historical events found.")
        return

    df = pd.DataFrame(events)
    
    st.dataframe(df, use_container_width=True)
    
    st.subheader("Explainability Features")
    st.info("Select an event above to view its SHAP/Captum feature importance graph (UI placeholder).")
