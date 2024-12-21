import dash_bootstrap_components as dbc
from dash import dcc
import pandas as pd

def create_filters(datasets, categories, dropdown_id_prefix="combined", combined_data=None):
    filter_components = []

    if dropdown_id_prefix == "combined":
        filter_components.extend([
            dbc.Label("Select Dataset(s):", className="text-dark"),
            dbc.Checklist(
                id=f"{dropdown_id_prefix}-dataset-checkbox",
                options=[{"label": f" {name}", "value": key} for key, name in datasets.items()],
                value=list(datasets.keys()),
                inline=False,
                switch=True,
                className="mb-3",
            )
        ])

    filter_components.extend([
        dbc.Label("Select Category:", className="text-dark"),
        dcc.Dropdown(
            id=f"{dropdown_id_prefix}-category-dropdown",
            options=[{"label": cat, "value": cat} for cat in categories] if categories else [],
            value=None,
            className="mb-3",
            placeholder="Select a category",
        ),
        dbc.Label("Select Metrics:", className="text-dark"),
        dcc.Dropdown(
            id=f"{dropdown_id_prefix}-metric-dropdown",
            options=[],
            value=[],
            multi=True,
            className="mb-3",
            placeholder="Select one or more metrics",
        ),
        dbc.Label("Select Date Range:", className="text-dark"),
        dcc.DatePickerRange(
            id=f"{dropdown_id_prefix}-date-range-picker",
            start_date=(
                combined_data["Week Start Date"].min().date()
                if dropdown_id_prefix == "combined" and combined_data is not None and not combined_data.empty
                else None
            ),
            end_date=(
                combined_data["Week Start Date"].max().date()
                if dropdown_id_prefix == "combined" and combined_data is not None and not combined_data.empty
                else None
            ),
            display_format="YYYY-MM-DD",
            className="mb-3",
        ),
    ])

    return dbc.Card(
        dbc.CardBody(filter_components),
        className="mb-4 shadow-sm",
    )
