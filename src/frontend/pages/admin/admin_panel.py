import streamlit as st
import pandas as pd

st.set_page_config(page_title="HeliosAI Admin Panel", layout="wide")

st.title("HeliosAI Admin Panel")
st.markdown("Administrative tools for user management, thresholds, and system health.")

tab1, tab2, tab3, tab4 = st.tabs(["Users & Roles", "Alert Thresholds", "Ingestion Status", "System Health"])

with tab1:
    st.header("User & Role Management")
    st.markdown("*(Mock UI)* View and edit user roles here.")
    st.button("Create New User")

with tab2:
    st.header("Alert Threshold Configuration")
    st.slider("Nowcast Confidence Gate", 0.0, 1.0, 0.85)
    st.slider("Forecast Probability Trigger", 0.0, 1.0, 0.75)
    st.button("Preview Historical Impact")
    st.button("Save Thresholds", type="primary")

with tab3:
    st.header("Ingestion Status")
    st.metric(label="SoLEXS Last Fetch", value="2026-07-11 09:42 UTC", delta="-2m")
    st.metric(label="HEL1OS Last Fetch", value="2026-07-11 09:42 UTC", delta="-2m")
    st.button("Manual Retrigger DAG")

with tab4:
    st.header("System Health & Metrics")
    st.markdown("Prometheus/Grafana integration view.")
    st.metric(label="API Latency (p95)", value="185ms")
    st.metric(label="Celery Queue Depth", value="0 tasks")
