from dash import html, dcc
import dash_bootstrap_components as dbc
from components.filters import create_filters
from components.graphs import create_graph
from components.tables import create_data_table
from data.preprocess import combined_data, categories_combined

def create_boys_girls_layout():
    return html.Div(
        [
            dbc.Container([
                dbc.Row(id="combined-kpi-cards", className="mb-4"),
                dbc.Row([
                    dbc.Col(
                        create_filters(
                            datasets={"data_boys": "Darul Ihsan Boys", "data_girls": "Darul Ihsan Girls"},
                            categories=categories_combined,
                            dropdown_id_prefix="combined",
                            combined_data=combined_data
                        ),
                        width=3
                    ),
                    dbc.Col([
                        dbc.Card(dbc.CardBody([create_graph("combined-graph", "")]), className="mb-4 shadow-sm"),

                        dbc.Button(
                            "Show/Hide Table",
                            id="combined-table-toggle-btn",
                            color="primary",
                            className="mb-2"
                        ),

                        dbc.Collapse(
                            dbc.Card(dbc.CardBody([
                                html.H5("Data Table", className="card-title text-primary"),
                                create_data_table(combined_data, "combined-data-table"),
                                html.Br(),
                                dbc.Button("Download CSV", id="combined-download-btn", color="primary", className="mt-2"),
                            ]), className="mb-4 shadow-sm"),
                            id="combined-table-collapse",
                            is_open=True
                        ),

                        dbc.Row([
                            dbc.Col(
                                dbc.Card(dbc.CardBody([
                                    html.H5("Bubble Chart by Metric (Aggregate)", className="card-title text-primary"),
                                    dcc.Graph(id="combined-bubble-chart")
                                ]), className="mb-4 shadow-sm"),
                                width=6
                            ),
                            dbc.Col(
                                dbc.Card(dbc.CardBody([
                                    html.H5("Summary & Narrative", className="card-title text-primary"),
                                    html.Div(id="combined-summary", style={"whiteSpace": "pre-wrap"})
                                ]), className="mb-4 shadow-sm"),
                                width=6
                            ),
                        ])
                    ], width=9),
                ]),
            ], fluid=True),
            dcc.Store(id="combined-filtered-data-store"),
            dcc.Download(id="combined-download-data")
        ],
        style={"backgroundColor": "#f7f7f7", "minHeight": "100vh"},
    )
