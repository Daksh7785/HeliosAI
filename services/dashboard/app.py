import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import requests
import pandas as pd
import os

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG], title="HeliosAI Dashboard")

API_URL = os.environ.get("API_URL", "http://backend:8000/api/v1")

app.layout = dbc.Container([
    dbc.Row(dbc.Col(html.H1("HeliosAI Dashboard", className="text-center mt-4 mb-4 text-primary"))),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Flare Catalogue"),
                dbc.CardBody([
                    html.Button("Refresh Catalogue", id="refresh-btn", className="btn btn-outline-info mb-3"),
                    html.Div(id="catalogue-table")
                ])
            ])
        ], width=12)
    ])
], fluid=True)

@app.callback(
    Output("catalogue-table", "children"),
    Input("refresh-btn", "n_clicks")
)
def update_catalogue(n_clicks):
    try:
        response = requests.get(f"{API_URL}/catalogue")
        if response.status_code == 200:
            data = response.json()
            if not data:
                return html.P("No flares in catalogue yet.")
            df = pd.DataFrame(data)
            return dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, className="table-dark")
        else:
            return html.P(f"Error fetching data: {response.status_code}")
    except Exception as e:
        return html.P(f"Could not connect to backend API: {e}")

if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=8050, debug=True)
