from dash import html, dcc
import dash_bootstrap_components as dbc
from components.filters import create_filters
from components.graphs import create_graph
from components.tables import create_data_table
from data.preprocess import data_properties, categories_properties

def create_properties_layout():
    return html.Div(
        [
            dbc.Container(fluid=True, children=[
                dbc.Row(id="properties-kpi-cards", className="mb-4"),
                dbc.Row([
                    dbc.Col(
                        create_filters(
                            datasets={"Properties": "Properties & Investment"},
                            categories=categories_properties,
                            dropdown_id_prefix="properties",
                            combined_data=None
                        ),
                        width=3, className="mb-4"
                    ),
                    dbc.Col([
                        dbc.Row([
                            dbc.Col(
                                dbc.Card(
                                    dbc.CardBody([create_graph("properties-graph", "")]),
                                    className="mb-4 shadow-sm"
                                ),
                                width=12
                            )
                        ]),

                        dbc.Button(
                            "Show/Hide Table",
                            id="properties-table-toggle-btn",
                            color="primary",
                            className="mb-2"
                        ),

                        dbc.Collapse(
                            dbc.Card(
                                dbc.CardBody([
                                    html.H5("Data Table", className="card-title text-primary"),
                                    create_data_table(data_properties, "properties-data-table"),
                                ]),
                                className="mb-4 shadow-sm"
                            ),
                            id="properties-table-collapse",
                            is_open=True
                        ),

                        dbc.Row([
                            dbc.Col(
                                dbc.Card(
                                    dbc.CardBody([
                                        html.H5("Summary & Narrative", className="card-title text-primary"),
                                        html.Div(id="properties-summary", style={"whiteSpace": "pre-wrap"})
                                    ]),
                                    className="mb-4 shadow-sm"
                                ),
                                width=12
                            ),
                        ]),
                    ], width=9),
                ], className="mb-4"),
            ]),
        ],
        style={"backgroundColor": "#f7f7f7", "minHeight": "100vh"}
    )
