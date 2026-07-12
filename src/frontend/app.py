import dash
from dash import dcc, html, Input, Output
import plotly.graph_objs as go
import requests
import pandas as pd

# External stylesheet for Google Fonts
external_stylesheets = [
    'https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Inter:wght@300;400;600&display=swap'
]

app = dash.Dash(__name__, title="HeliosAI Dashboard", external_stylesheets=external_stylesheets)

# Custom CSS for Glassmorphism and Dark Theme
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            body {
                background: linear-gradient(135deg, #0a0a1a 0%, #1a1a2e 100%);
                color: #e0e0e0;
                font-family: 'Inter', sans-serif;
                margin: 0;
                padding: 20px;
                min-height: 100vh;
            }
            h1, h2, h3 {
                font-family: 'Orbitron', sans-serif;
                color: #00f3ff;
                text-shadow: 0 0 10px rgba(0, 243, 255, 0.5);
            }
            .glass-container {
                background: rgba(255, 255, 255, 0.03);
                backdrop-filter: blur(12px);
                -webkit-backdrop-filter: blur(12px);
                border: 1px solid rgba(255, 255, 255, 0.05);
                border-radius: 16px;
                padding: 24px;
                margin-bottom: 24px;
                box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
            }
            .alert-box {
                padding: 16px 24px;
                border-radius: 12px;
                font-family: 'Orbitron', sans-serif;
                font-weight: bold;
                font-size: 1.2rem;
                text-align: center;
                transition: all 0.5s ease;
                letter-spacing: 2px;
                text-transform: uppercase;
                box-shadow: 0 0 20px rgba(0,0,0,0.5);
            }
            .table-container {
                overflow-x: auto;
            }
            table {
                width: 100%;
                border-collapse: collapse;
                margin-top: 10px;
            }
            th {
                background: rgba(0, 243, 255, 0.1);
                color: #00f3ff;
                padding: 12px;
                text-align: left;
                font-weight: 600;
                border-bottom: 1px solid rgba(0, 243, 255, 0.3);
            }
            td {
                padding: 12px;
                border-bottom: 1px solid rgba(255, 255, 255, 0.05);
            }
            tr:hover td {
                background: rgba(255, 255, 255, 0.05);
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

app.layout = html.Div([
    html.Div([
        html.H1("HELIOS AI"),
        html.P("SPACE WEATHER INTELLIGENCE PLATFORM", style={'letterSpacing': '4px', 'opacity': '0.7', 'marginTop': '-10px', 'marginBottom': '30px'})
    ], style={'textAlign': 'center'}),
    
    html.Div(id='forecast-alert', className='alert-box', style={'display': 'none'}),
    
    html.Div([
        html.H3("LIVE TELEMETRY & FORECAST"),
        dcc.Graph(id='live-flux-graph', config={'displayModeBar': False}),
        html.Div(id='xai-insights', style={'marginTop': '10px', 'color': '#ffaa00', 'fontFamily': 'Orbitron', 'fontSize': '0.9rem'}),
        dcc.Interval(
            id='interval-component',
            interval=5*1000,
            n_intervals=0
        )
    ], className='glass-container'),
    
    html.Div([
        html.H3("RECENT FLARE EVENTS"),
        html.Div(id='flare-table', className='table-container')
    ], className='glass-container')
])

@app.callback(
    [Output('live-flux-graph', 'figure'),
     Output('forecast-alert', 'children'),
     Output('forecast-alert', 'style'),
     Output('xai-insights', 'children')],
    Input('interval-component', 'n_intervals')
)
def update_graph_live(n):
    alert_text = "SYSTEM NOMINAL: NO FLARE IMMINENT"
    alert_style = {
        'display': 'block', 
        'backgroundColor': 'rgba(0, 255, 136, 0.1)', 
        'color': '#00ff88',
        'border': '1px solid #00ff88',
        'textShadow': '0 0 10px rgba(0, 255, 136, 0.5)'
    }
    
    try:
        response = requests.get('http://127.0.0.1:8000/api/v1/telemetry/recent?limit=120')
        if response.status_code == 200:
            data = response.json()
            if not data:
                return go.Figure(layout=go.Layout(template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')), alert_text, alert_style, ""
            
            df = pd.DataFrame(data)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            
            fig = go.Figure()
            
            # Gradients and neon lines for flux
            fig.add_trace(go.Scatter(
                x=df['timestamp'], y=df['solexs_flux'], 
                name='SoLEXS (1-30keV)', 
                yaxis='y1',
                line=dict(color='#00f3ff', width=2),
                fill='tozeroy',
                fillcolor='rgba(0, 243, 255, 0.1)'
            ))
            
            fig.add_trace(go.Scatter(
                x=df['timestamp'], y=df['hel1os_flux'], 
                name='HEL1OS (20-150keV)', 
                yaxis='y1',
                line=dict(color='#ff00ff', width=2),
                fill='tozeroy',
                fillcolor='rgba(255, 0, 255, 0.05)'
            ))
            
            xai_text = ""
            if 'forecast_probability' in df.columns:
                fig.add_trace(go.Scatter(
                    x=df['timestamp'], y=df['forecast_probability'], 
                    name='Forecast Prob', 
                    line=dict(dash='dash', color='#ffaa00', width=2), 
                    yaxis='y2'
                ))
                
                latest_prob = df['forecast_probability'].iloc[-1]
                if latest_prob is not None and latest_prob > 0.5:
                    if 'xai_top_features' in df.columns and df['xai_top_features'].iloc[-1]:
                        import json
                        try:
                            top_feats = json.loads(df['xai_top_features'].iloc[-1])
                            xai_text = f"► XAI DRIVERS: {', '.join(top_feats).replace('_', ' ').upper()}"
                        except:
                            pass
                if latest_prob is not None and latest_prob > 0.8:
                    alert_text = f"CRITICAL WARNING: HIGH FLARE PROBABILITY ({latest_prob:.1%})"
                    alert_style.update({
                        'backgroundColor': 'rgba(255, 51, 51, 0.15)',
                        'color': '#ff3333',
                        'border': '1px solid #ff3333',
                        'textShadow': '0 0 15px rgba(255, 51, 51, 0.8)'
                    })
                elif latest_prob is not None and latest_prob > 0.5:
                    alert_text = f"CAUTION: ELEVATED FLARE PROBABILITY ({latest_prob:.1%})"
                    alert_style.update({
                        'backgroundColor': 'rgba(255, 170, 0, 0.15)',
                        'color': '#ffaa00',
                        'border': '1px solid #ffaa00',
                        'textShadow': '0 0 15px rgba(255, 170, 0, 0.8)'
                    })
            
            # Highlight flare candidates with a glow effect
            if 'is_flare_candidate' in df.columns:
                flare_df = df[df['is_flare_candidate'] == True]
                if not flare_df.empty:
                    fig.add_trace(go.Scatter(
                        x=flare_df['timestamp'], 
                        y=flare_df['solexs_flux'], 
                        mode='markers', 
                        marker=dict(color='#ff3333', size=10, symbol='circle', line=dict(color='#ffffff', width=1)),
                        name='Flare Detected'
                    ))
            
            fig.update_layout(
                template='plotly_dark',
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=20, r=20, t=40, b=20),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)', title='UTC Time'),
                yaxis=dict(title='X-ray Flux (W/m²)', type='log', showgrid=True, gridcolor='rgba(255,255,255,0.05)', exponentformat='e'),
                yaxis2=dict(title='Prediction Probability', overlaying='y', side='right', range=[0, 1], showgrid=False)
            )
            return fig, alert_text, alert_style, xai_text
    except Exception as e:
        print(f"Error fetching telemetry: {e}")
        
    return go.Figure(layout=go.Layout(template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')), alert_text, alert_style, ""

@app.callback(
    Output('flare-table', 'children'),
    Input('interval-component', 'n_intervals')
)
def update_table_live(n):
    try:
        response = requests.get('http://127.0.0.1:8000/api/v1/catalogue/recent?limit=5')
        if response.status_code == 200:
            data = response.json()
            if not data:
                return html.P("No recent anomalies detected.", style={'opacity': '0.7'})
            
            df = pd.DataFrame(data)
            
            return html.Table([
                html.Thead(
                    html.Tr([html.Th(col.replace('_', ' ').title()) for col in df.columns])
                ),
                html.Tbody([
                    html.Tr([
                        html.Td(str(df.iloc[i][col])) for col in df.columns
                    ]) for i in range(len(df))
                ])
            ])
    except Exception as e:
        print(f"Error fetching catalogue: {e}")
        
    return html.P("System Error: Unable to load catalogue.", style={'color': '#ff3333'})

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8050)
