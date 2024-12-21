import dash_bootstrap_components as dbc
from dash import html

def generate_kpi_cards(kpis):
    current_week, pct_change, avg, max_val, min_val = kpis
    pct_icon = "fas fa-minus"
    if pct_change is not None:
        pct_icon = "fas fa-arrow-up" if pct_change >= 0 else "fas fa-arrow-down"

    kpi_definitions = [
        {"title": "This Week's Total Value", "value": f"{current_week:,.2f}" if current_week is not None else "N/A", "icon": "fas fa-calendar-alt"},
        {"title": "% Change from Last Week", "value": f"{pct_change:+.2f}%" if pct_change is not None else "N/A", "icon": pct_icon},
        {"title": "Overall Average Value", "value": f"{avg:,.2f}" if avg is not None else "N/A", "icon": "fas fa-chart-line"},
        {"title": "Max Value", "value": f"{max_val:,.2f}" if max_val is not None else "N/A", "icon": "fas fa-arrow-up"},
        {"title": "Min Value", "value": f"{min_val:,.2f}" if min_val is not None else "N/A", "icon": "fas fa-arrow-down"},
    ]

    return dbc.Row(
        [dbc.Col(
            dbc.Card(
                dbc.CardBody([
                    html.Div([
                        html.I(className=f"{kpi['icon']} mb-2"),
                        html.H6(kpi["title"], className="card-title"),
                        html.H4(kpi["value"], className="card-text"),
                    ], className="text-center"),
                ]),
                className="kpi-card",
            ), width=2
        ) for kpi in kpi_definitions],
        justify="start"
    )
