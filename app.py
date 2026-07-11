import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
import joblib
import sys

# Ensure src modules can be imported
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
from data_loader import load_and_merge_data
from flare_detector import detect_flares
from forecaster import create_features_and_labels

st.set_page_config(page_title="HeliosAI Solar Flare Dashboard", layout="wide")

st.title("☀️ HeliosAI: Solar Flare Nowcasting & Forecasting")
st.markdown("Monitoring Soft X-ray (SoLEXS) and Hard X-ray (HEL1OS) data from Aditya-L1")

@st.cache_data
def load_data():
    solexs_path = 'data/solexs_simulated.csv'
    helios_path = 'data/helios_simulated.csv'
    if not os.path.exists(solexs_path) or not os.path.exists(helios_path):
        from data_loader import generate_simulated_data
        generate_simulated_data()
    return load_and_merge_data(solexs_path, helios_path)

@st.cache_resource
def load_model():
    model_path = 'models/xgboost_forecaster.pkl'
    if os.path.exists(model_path):
        model = joblib.load(model_path)
        features = joblib.load(model_path.replace('.pkl', '_features.pkl'))
        return model, features
    return None, None

df = load_data()
model, model_features = load_model()

# Sidebar controls
st.sidebar.header("Controls")
time_range = st.sidebar.slider("Select Time Range (hours from start)", 0, 24, (0, 24))

start_time = df['timestamp'].min() + pd.Timedelta(hours=time_range[0])
end_time = df['timestamp'].min() + pd.Timedelta(hours=time_range[1])

df_filtered = df[(df['timestamp'] >= start_time) & (df['timestamp'] <= end_time)]

# Run Nowcasting
with st.spinner('Running Nowcast Algorithm...'):
    df_nowcast, catalogue = detect_flares(df_filtered)

# Run Forecasting
df_forecast_prob = None
if model:
    with st.spinner('Running Forecast Model...'):
        # For visualization, we just need features, no need to exclude flare times
        # Passing an empty catalogue since we only want features
        df_feat = create_features_and_labels(df_filtered, pd.DataFrame(columns=['start_time', 'end_time']))
        
        # Only predict if we have all features
        missing_feats = [f for f in model_features if f not in df_feat.columns]
        if not missing_feats:
            probs = model.predict_proba(df_feat[model_features])[:, 1]
            df_feat['flare_probability'] = probs
            df_forecast_prob = df_feat[['timestamp', 'flare_probability']]

# Create Plotly figure
fig = make_subplots(rows=3, cols=1, shared_xaxes=True, 
                    vertical_spacing=0.05,
                    subplot_titles=('Soft X-ray (SoLEXS)', 'Hard X-ray (HEL1OS)', 'Flare Probability (Forecast)'))

# SoLEXS Plot
fig.add_trace(go.Scatter(x=df_nowcast['timestamp'], y=df_nowcast['solexs_flux'], name='SoLEXS Flux', line=dict(color='blue')), row=1, col=1)
# Highlight nowcasted flares in Soft X-ray
flare_soft = df_nowcast[df_nowcast['soft_flare_detected']]
fig.add_trace(go.Scatter(x=flare_soft['timestamp'], y=flare_soft['solexs_flux'], mode='markers', name='Nowcast (Soft)', marker=dict(color='red', size=4)), row=1, col=1)

# HEL1OS Plot
fig.add_trace(go.Scatter(x=df_nowcast['timestamp'], y=df_nowcast['helios_flux'], name='HEL1OS Flux', line=dict(color='orange')), row=2, col=1)
# Highlight nowcasted flares in Hard X-ray
flare_hard = df_nowcast[df_nowcast['hard_flare_detected']]
fig.add_trace(go.Scatter(x=flare_hard['timestamp'], y=flare_hard['helios_flux'], mode='markers', name='Nowcast (Hard)', marker=dict(color='red', size=4)), row=2, col=1)

# Forecast Probability Plot
if df_forecast_prob is not None:
    fig.add_trace(go.Scatter(x=df_forecast_prob['timestamp'], y=df_forecast_prob['flare_probability'], name='Probability', line=dict(color='green')), row=3, col=1)
    # Threshold line
    fig.add_hline(y=0.5, line_dash="dash", line_color="red", row=3, col=1, annotation_text="Trigger Alert (50%)")

fig.update_layout(height=800, title_text="Light Curves and Active Detections", hovermode="x unified")
fig.update_yaxes(title_text="Flux (W/m^2)", row=1, col=1, type="log")
fig.update_yaxes(title_text="Flux (W/m^2)", row=2, col=1, type="log")
fig.update_yaxes(title_text="Probability", row=3, col=1, range=[0, 1.1])

st.plotly_chart(fig, use_container_width=True)

# Master Catalogue Display
st.subheader("Nowcasted Master Flare Catalogue")
if not catalogue.empty:
    st.dataframe(catalogue)
else:
    st.info("No flares detected in the selected time range.")
