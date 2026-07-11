import streamlit as st

st.set_page_config(
    page_title="HeliosAI Space Weather Dashboard",
    page_icon="☀️",
    layout="wide"
)

st.title("☀️ HeliosAI Intelligence Platform")

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Real-time Monitor", "Historical Catalogue"])

if page == "Real-time Monitor":
    from views.realtime import render_realtime
    render_realtime()
elif page == "Historical Catalogue":
    from views.historical import render_historical
    render_historical()
