import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

dash.register_page(__name__, path='/')

layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H2("Live Dashboard"), width=12)
    ]),
    dbc.Row([
        dbc.Col(id="alert-banner", width=12)
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='light-curve-panel', style={"height": "60vh"})
        ], width=9),
        dbc.Col([
            html.H4("Forecast Probability"),
            dcc.Graph(id='forecast-gauge'),
            html.H4("Recent Events"),
            html.Div(id='recent-events-list')
        ], width=3)
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='hardness-ratio-strip', style={"height": "15vh"})
        ], width=12)
    ]),
    dcc.Interval(id='live-update-interval', interval=5000, n_intervals=0)
], fluid=True)

@callback(
    Output('light-curve-panel', 'figure'),
    Output('hardness-ratio-strip', 'figure'),
    Output('forecast-gauge', 'figure'),
    Input('live-update-interval', 'n_intervals')
)
def update_dashboard(n):
    # Mock figures for now. LTTB down-sampling will be implemented here per Doc 40.
    fig_lc = go.Figure()
    fig_lc.add_trace(go.Scattergl(x=[1, 2, 3], y=[4, 1, 2], name="SoLEXS"))
    fig_lc.add_trace(go.Scattergl(x=[1, 2, 3], y=[2, 4, 1], name="HEL1OS"))
    fig_lc.update_layout(title="Dual-Band Light Curves", yaxis_type="log")

    fig_hr = go.Figure()
    fig_hr.add_trace(go.Scattergl(x=[1, 2, 3], y=[2, 0.25, 2], name="Hardness Ratio"))
    fig_hr.update_layout(margin=dict(t=10, b=10, l=10, r=10))

    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=15,
        title={'text': "P(Flare > M) next 30m"},
        gauge={'axis': {'range': [0, 100]}}
    ))
    return fig_lc, fig_hr, fig_gauge
