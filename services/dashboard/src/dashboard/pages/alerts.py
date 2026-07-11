import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

# Doc 42: Alert Dispatcher Interface
dash.register_page(__name__, path='/alerts', name='Alert Dispatcher')

layout = dbc.Container([
    html.H2("Alert Dispatcher Configuration", className="mt-4 mb-4"),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Webhook Subscriptions"),
                dbc.CardBody([
                    dbc.Input(placeholder="Enter Webhook URL (e.g. Slack/Teams)", className="mb-3"),
                    dcc.Dropdown(
                        options=[
                            {'label': 'All Events', 'value': 'all'},
                            {'label': 'M-Class & Above', 'value': 'm_class'},
                            {'label': 'X-Class Only', 'value': 'x_class'}
                        ],
                        placeholder="Select Trigger Threshold",
                        className="mb-3"
                    ),
                    dbc.Button("Add Subscription", color="success")
                ])
            ], className="mb-4"),
            
            dbc.Card([
                dbc.CardHeader("Active Subscriptions"),
                dbc.CardBody([
                    html.Ul([
                        html.Li("Slack Channel: #helios-alerts (M-Class & Above)")
                    ])
                ])
            ])
        ], md=6)
    ])
], fluid=True)
