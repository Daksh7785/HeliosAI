from dash import html, dcc
import dash_bootstrap_components as dbc

def create_layout() -> html.Div:
    """
    Creates the main layout for the HeliosAI dashboard.
    """
    navbar = dbc.NavbarSimple(
        brand="HeliosAI",
        brand_href="#",
        color="primary",
        dark=True,
    )
    
    content = dbc.Container([
        dbc.Row([
            dbc.Col(html.H2("Real-time Solar Flare Forecasting"), className="mt-4")
        ]),
        dbc.Row([
            dbc.Col(
                dbc.Card(
                    dbc.CardBody([
                        html.H4("Current Forecast", className="card-title"),
                        html.P("Status: Normal", className="card-text text-success", id="forecast-status"),
                    ])
                ),
                width=4
            ),
            dbc.Col(
                dbc.Card(
                    dbc.CardBody([
                        html.H4("Telemetry", className="card-title"),
                        dcc.Graph(id="live-telemetry-graph")
                    ])
                ),
                width=8
            )
        ], className="mt-4")
    ], fluid=True)
    
    return html.Div([navbar, content])
