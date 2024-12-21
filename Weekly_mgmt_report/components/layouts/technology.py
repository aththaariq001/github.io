from dash import html, dcc
import dash_bootstrap_components as dbc
from components.filters import create_filters
from components.graphs import create_graph
from components.tables import create_data_table
from data.preprocess import data_tech, categories_tech

def create_technology_layout():
    return html.Div(
        [
            dbc.Container([
                dbc.Row(id="tech-kpi-cards", className="mb-4"),

                dbc.Row([
                    dbc.Col(
                        create_filters(
                            datasets={"Technology": "Technology"},
                            categories=categories_tech,
                            dropdown_id_prefix="tech",
                            combined_data=None
                        ),
                        width=3
                    ),
                    dbc.Col([
                        dbc.Card(dbc.CardBody([create_graph("tech-graph", "")]), className="mb-4 shadow-sm"),

                        dbc.Button(
                            "Show/Hide Table",
                            id="tech-table-toggle-btn",
                            color="primary",
                            className="mb-2"
                        ),

                        dbc.Collapse(
                            dbc.Card(dbc.CardBody([
                                html.H5("Data Table", className="card-title text-primary"),
                                create_data_table(data_tech, "tech-data-table"),
                            ]), className="mb-4 shadow-sm"),
                            id="tech-table-collapse",
                            is_open=True
                        ),

                        dbc.Row([
                            dbc.Col(
                                dbc.Card(dbc.CardBody([
                                    html.H5("Radar Chart of Metrics", className="card-title text-primary"),
                                    dcc.Graph(id="tech-radar-chart")
                                ]), className="mb-4 shadow-sm"),
                                width=6
                            ),
                            dbc.Col(
                                dbc.Card(dbc.CardBody([
                                    html.H5("Summary & Narrative", className="card-title text-primary"),
                                    html.Div(id="tech-summary", style={"whiteSpace": "pre-wrap"})
                                ]), className="mb-4 shadow-sm"),
                                width=6
                            ),
                        ]),
                    ], width=9),
                ]),
            ], fluid=True),
        ],
        style={"backgroundColor": "#f7f7f7", "minHeight": "100vh"},
    )
