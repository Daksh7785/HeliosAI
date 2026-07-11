import dash
import dash_bootstrap_components as dbc
from dashboard.layout.main_layout import create_layout

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.DARKLY],
    suppress_callback_exceptions=True
)

app.title = "HeliosAI - Solar Flare Forecasting"
app.layout = create_layout()

if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=8050)
