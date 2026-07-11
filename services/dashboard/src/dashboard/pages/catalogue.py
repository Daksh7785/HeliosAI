import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import logging

logger = logging.getLogger(__name__)

# Docs 39 & 43: Dashboard & Catalogue Explorer
dash.register_page(__name__, path='/catalogue', name='Catalogue Explorer')

layout = dbc.Container([
    html.H2("Flare Event Catalogue", className="mt-4 mb-4"),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Filter Events"),
                dbc.CardBody([
                    dcc.Dropdown(
                        id='class-filter',
                        options=[
                            {'label': 'X-Class', 'value': 'X'},
                            {'label': 'M-Class', 'value': 'M'},
                            {'label': 'C-Class', 'value': 'C'}
                        ],
                        placeholder="Select Flare Class",
                        className="mb-3"
                    ),
                    dcc.DatePickerRange(
                        id='date-filter',
                        className="mb-3"
                    ),
                    dbc.Button("Apply Filters", color="primary", className="w-100")
                ])
            ])
        ], md=3),
        
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Master Catalogue"),
                dbc.CardBody([
                    html.Div(id='catalogue-table-container', children=[
                        dbc.Table.from_dataframe(
                            # Mock Data
                            import pandas as pd
                            pd.DataFrame({
                                'Event ID': ['evt_001', 'evt_002'],
                                'Onset': ['2026-07-03T01:42Z', '2026-07-04T12:00Z'],
                                'Class': ['M2.4', 'X1.1'],
                                'Confidence': ['0.91', '0.98'],
                                'Status': ['Promoted', 'Promoted']
                            }),
                            striped=True, bordered=True, hover=True
                        )
                    ])
                ])
            ])
        ], md=9)
    ])
], fluid=True)
