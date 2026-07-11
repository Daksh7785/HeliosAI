import dash
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc

app = Dash(
    __name__,
    use_pages=True,
    external_stylesheets=[dbc.themes.SLATE],
    suppress_callback_exceptions=True
)

app.layout = html.Div([
    dcc.Location(id="url"),
    dbc.NavbarSimple(
        brand="HeliosAI Dashboard",
        brand_href="/",
        color="dark",
        dark=True,
        children=[
            dbc.NavItem(dbc.NavLink("Dashboard", href="/")),
            dbc.NavItem(dbc.NavLink("Catalogue", href="/catalogue")),
            dbc.NavItem(dbc.NavLink("Alerts", href="/alerts")),
            dbc.NavItem(dbc.NavLink("Admin", href="/admin")),
        ]
    ),
    dash.page_container
])

if __name__ == '__main__':
    app.run_server(debug=True, port=8050)
