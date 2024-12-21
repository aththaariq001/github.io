from dash import html
import dash_bootstrap_components as dbc

sidebar_style = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "1rem",
    "background-color": "#2c3e50",
    "overflow": "auto",
    "color": "#ecf0f1",
    "transition": "width 0.4s ease, padding 0.4s ease",
}

def create_sidebar():
    sidebar_content = [
        html.H2("MTFA Dashboard", className="display-6", id="sidebar-title"),
        html.Hr(className="bg-light"),
        dbc.Nav(
            [
                dbc.NavLink(
                    [html.I(className="fas fa-users me-2"), "Boys & Girls Metrics"],
                    href="/boys-girls",
                    active="exact",
                    className="text-white",
                ),
                dbc.NavLink(
                    [html.I(className="fas fa-desktop me-2"), "Technology Metrics"],
                    href="/technology",
                    active="exact",
                    className="text-white",
                ),
                dbc.NavLink(
                    [html.I(className="fas fa-building me-2"), "Properties & Investment"],
                    href="/properties-investment",
                    active="exact",
                    className="text-white",
                ),
            ],
            vertical=True,
            pills=True,
            id="nav-links",
            className="mt-3",
        ),
    ]
    return html.Div(sidebar_content, id="sidebar", style=sidebar_style)
