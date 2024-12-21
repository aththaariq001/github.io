from dash import Dash, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.io as pio
import pandas as pd
import logging

# Import components and data
from components.sidebar import create_sidebar
from components.layouts.boys_girls import create_boys_girls_layout
from components.layouts.technology import create_technology_layout
from components.layouts.properties import create_properties_layout

from data.preprocess import (
    combined_data, data_boys, data_girls, data_tech, data_properties,
    categories_combined, category_metric_map_combined,
    category_metric_map_tech, category_metric_map_properties
)
from utils.kpi_calculations import calculate_kpis
from components.kpis import generate_kpi_cards

import plotly.express as px
import plotly.graph_objects as go
import json
import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

# Load custom Plotly template
with open("templates/plotly_custom.json", "r") as f:
    custom_template = json.load(f)
pio.templates["custom_flatly"] = custom_template

app = Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.FLATLY,
        "https://use.fontawesome.com/releases/v5.8.1/css/all.css",
        "https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600&display=swap",
    ],
    suppress_callback_exceptions=True,
)
app.title = "Management Report Dashboard"


sidebar_toggle = html.Div(
    dbc.Button(
        html.I(className="fas fa-bars"),
        color="secondary",
        id="btn_sidebar",
        n_clicks=0,
    ),
    style={
        "position": "fixed",
        "bottom": "1rem",
        "left": "1rem",
        "zIndex": 1000,
    },
)

content_style = {
    "margin-left": "16rem",
    "padding": "2rem 1rem",
    "transition": "margin-left 0.5s",
    "backgroundColor": "#f7f7f7",
    "minHeight": "100vh",
}

app.layout = html.Div(
    [
        dcc.Location(id="url"),
        create_sidebar(),
        sidebar_toggle,
        html.Div(id="page-content", style=content_style),
    ],
    id="html",
    **{"data-theme": "light"}
)


# ------------------------------
# Page navigation callback
# ------------------------------
@app.callback(Output("page-content", "children"), Input("url", "pathname"))
def display_page(pathname):
    if pathname == "/boys-girls":
        return create_boys_girls_layout()
    elif pathname == "/technology":
        return create_technology_layout()
    elif pathname == "/properties-investment":
        return create_properties_layout()
    else:
        return html.Div(
            dbc.Container([
                html.H1("Welcome to the Management Report Dashboard", className="text-center mb-4 text-primary"),
                html.P("Use the sidebar to navigate to different sections of the dashboard.", className="lead text-center text-dark"),
            ], fluid=True),
            style={"textAlign": "center", "backgroundColor": "#f7f7f7", "minHeight": "100vh"},
        )

# ------------------------------
# Sidebar toggle callback
# ------------------------------
@app.callback(
    [Output("sidebar", "style"), Output("page-content", "style"), Output("btn_sidebar", "children")],
    [Input("btn_sidebar", "n_clicks")],
    [State("sidebar", "style"), State("page-content", "style")],
)
def toggle_sidebar(n_clicks, sidebar_style, curr_content_style):
    if n_clicks and n_clicks % 2 == 1:
        sidebar_style.update({"width": "0", "padding": "0"})
        curr_content_style.update({"margin-left": "0"})
        button_icon = html.I(className="fas fa-bars")
    else:
        sidebar_style.update({"width": "16rem", "padding": "1rem"})
        curr_content_style.update({"margin-left": "16rem"})
        button_icon = html.I(className="fas fa-times")
    return sidebar_style, curr_content_style, button_icon

# ------------------------------
# Boys & Girls Callbacks
# ------------------------------

@app.callback(
    Output("combined-table-collapse", "is_open"),
    Input("combined-table-toggle-btn", "n_clicks"),
    State("combined-table-collapse", "is_open")
)
def toggle_combined_table_collapse(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open

@app.callback(Output("combined-metric-dropdown", "options"), Input("combined-category-dropdown", "value"))
def update_combined_metric_dropdown(category):
    return [{"label": metric, "value": metric} for metric in category_metric_map_combined.get(category, [])] if category else []

@app.callback(
    [
        Output("combined-graph", "figure"),
        Output("combined-data-table", "data"),
        Output("combined-kpi-cards", "children"),
        Output("combined-bubble-chart", "figure"),
        Output("combined-summary", "children"),
        Output("combined-filtered-data-store", "data"),
    ],
    [
        Input("combined-dataset-checkbox", "value"),
        Input("combined-category-dropdown", "value"),
        Input("combined-metric-dropdown", "value"),
        Input("combined-date-range-picker", "start_date"),
        Input("combined-date-range-picker", "end_date"),
    ],
)
def update_combined_graph_table_kpis(selected_datasets, category, metrics, start_date, end_date):
    if not selected_datasets or not category or not metrics:
        empty_fig = go.Figure(
            layout=go.Layout(
                title="Please select dataset, category, and metrics to display data",
                template="custom_flatly",
            )
        )
        return empty_fig, [], [], go.Figure(), "", []

    filtered_data = pd.concat([
        df[
            (df["Category"] == category) &
            (df["Metric"].isin(metrics)) &
            (df["Week Start Date"] >= pd.to_datetime(start_date)) &
            (df["Week Start Date"] <= pd.to_datetime(end_date))
        ] for key, df in {"data_boys": data_boys, "data_girls": data_girls}.items() if key in selected_datasets
    ]) if selected_datasets else pd.DataFrame()

    if filtered_data.empty:
        empty_fig = go.Figure(layout=go.Layout(title="No Data Available", template="custom_flatly"))
        return empty_fig, [], [], go.Figure(), "", []

    kpis = calculate_kpis(filtered_data)
    kpi_cards = generate_kpi_cards(kpis)

    filtered_data = filtered_data.sort_values("Week Start Date")
    rolling_window = 4
    filtered_data["Rolling_Avg"] = filtered_data.groupby(["Source", "Metric"])["Value"].transform(lambda x: x.rolling(rolling_window, min_periods=1).mean())

    avg_value = filtered_data["Value"].mean()

    fig = px.line(
        filtered_data,
        x="Week Start Date",
        y="Value",
        color="Source",
        line_dash="Metric",
        title=f"{category} Metrics Over Time",
        markers=True,
        template="custom_flatly",
        hover_data={"Week Start Date": True, "Value": ":.2f", "Metric": True, "Source": True}
    )

    for (src, met), grp in filtered_data.groupby(["Source", "Metric"]):
        fig.add_trace(
            go.Scatter(
                x=grp["Week Start Date"],
                y=grp["Rolling_Avg"],
                mode="lines",
                line=dict(dash="dot", width=2),
                name=f"{src}-{met} (Rolling Avg)"
            )
        )

    fig.add_hline(y=avg_value, line_width=2, line_dash="dash", line_color="red")
    fig.add_annotation(
        x=filtered_data["Week Start Date"].iloc[-1],
        y=avg_value,
        text="Overall Avg",
        showarrow=True,
        arrowhead=2,
        ax=0,
        ay=-40,
        font=dict(color="red")
    )

    fig.update_layout(legend_title_text='Source')
    fig.update_traces(marker=dict(size=6), line=dict(width=2))
    fig.update_layout(transition=dict(duration=500, easing='cubic-in-out'))

    # Bubble chart
    agg_data = filtered_data.groupby("Metric", as_index=False)["Value"].sum()
    bubble_fig = px.scatter(
        agg_data,
        x="Metric",
        y="Value",
        size="Value",
        color="Metric",
        hover_data={"Value": ":.2f"},
        template="custom_flatly",
        title="Aggregate Values by Metric"
    )

    current_week, pct_change, avg_val, max_val, min_val = kpis
    if pct_change is not None:
        if pct_change < 0:
            summary_text = "🔴 Performance decline, corrective action needed\n"
        else:
            summary_text = "🟢 Performance improving, keep it up!\n"
    else:
        summary_text = "No previous data for comparison.\n"

    summary_text += f"\nFor the selected metrics and category ({category}), the average value is {avg_val:.2f}, with a maximum of {max_val:.2f} and minimum of {min_val:.2f}.\n"
    if pct_change is not None:
        summary_text += f"Current performance changed by {pct_change:+.2f}% compared to the previous period."

    return fig, filtered_data.to_dict("records"), kpi_cards, bubble_fig, summary_text, filtered_data.to_dict("records")


@app.callback(
    Output("combined-download-data", "data"),
    Input("combined-download-btn", "n_clicks"),
    State("combined-filtered-data-store", "data"),
    prevent_initial_call=True
)
def download_combined_data(n_clicks, data):
    if data:
        df = pd.DataFrame(data)
        csv_string = df.to_csv(index=False, encoding='utf-8')
        return dict(content=csv_string, filename="filtered_data.csv")
    return None

# ------------------------------
# Technology Callbacks
# ------------------------------
@app.callback(
    Output("tech-table-collapse", "is_open"),
    Input("tech-table-toggle-btn", "n_clicks"),
    State("tech-table-collapse", "is_open")
)
def toggle_tech_table_collapse(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open

@app.callback(Output("tech-metric-dropdown", "options"), Input("tech-category-dropdown", "value"))
def update_tech_metric_dropdown(category):
    return [{"label": metric, "value": metric} for metric in category_metric_map_tech.get(category, [])] if category else []

@app.callback(
    [
        Output("tech-graph", "figure"),
        Output("tech-data-table", "data"),
        Output("tech-kpi-cards", "children"),
        Output("tech-radar-chart", "figure"),
        Output("tech-summary", "children"),
    ],
    [
        Input("tech-category-dropdown", "value"),
        Input("tech-metric-dropdown", "value"),
        Input("tech-date-range-picker", "start_date"),
        Input("tech-date-range-picker", "end_date"),
    ],
)
def update_tech_graph_table_kpis(category, metrics, start_date, end_date):
    if not category or not metrics:
        empty_fig = go.Figure(layout=go.Layout(title="Please select category and metrics to display data", template="custom_flatly"))
        return empty_fig, [], [], go.Figure(), ""

    filtered_data = data_tech[
        (data_tech["Category"] == category) &
        (data_tech["Metric"].isin(metrics)) &
        (data_tech["Week Start Date"] >= pd.to_datetime(start_date)) &
        (data_tech["Week Start Date"] <= pd.to_datetime(end_date))
    ]

    if filtered_data.empty:
        empty_fig = go.Figure(layout=go.Layout(title="No Data Available", template="custom_flatly"))
        return empty_fig, [], [], go.Figure(), ""

    kpis = calculate_kpis(filtered_data)
    kpi_cards = generate_kpi_cards(kpis)

    filtered_data = filtered_data.sort_values("Week Start Date")
    rolling_window = 4
    filtered_data["Rolling_Avg"] = filtered_data.groupby(["Metric"])["Value"].transform(lambda x: x.rolling(rolling_window, min_periods=1).mean())

    avg_value = filtered_data["Value"].mean()

    fig = px.line(
        filtered_data,
        x="Week Start Date",
        y="Value",
        color="Metric",
        title=f"{category} Metrics (Technology)",
        markers=True,
        template="custom_flatly",
        hover_data={"Week Start Date": True, "Value": ":.2f", "Metric": True}
    )

    for met, grp in filtered_data.groupby("Metric"):
        fig.add_trace(
            go.Scatter(
                x=grp["Week Start Date"],
                y=grp["Rolling_Avg"],
                mode="lines",
                line=dict(dash="dot", width=2),
                name=f"{met} (Rolling Avg)"
            )
        )

    fig.add_hline(y=avg_value, line_width=2, line_dash="dash", line_color="red")
    fig.add_annotation(
        x=filtered_data["Week Start Date"].iloc[-1],
        y=avg_value,
        text="Overall Avg",
        showarrow=True,
        arrowhead=2,
        ax=0,
        ay=-40,
        font=dict(color="red")
    )

    fig.update_layout(legend_title_text='Metric')
    fig.update_traces(marker=dict(size=6), line=dict(width=2))
    fig.update_layout(transition=dict(duration=500, easing='cubic-in-out'))

    # Radar chart
    radar_data = filtered_data.groupby("Metric")["Value"].mean().reset_index()
    radar_data = pd.concat([radar_data, radar_data.iloc[[0]]])
    radar_fig = go.Figure()
    radar_fig.add_trace(go.Scatterpolar(
        r=radar_data["Value"],
        theta=radar_data["Metric"],
        fill='toself',
        name='Avg Value'
    ))
    radar_fig.update_layout(
        polar=dict(radialaxis=dict(visible=True)),
        showlegend=False,
        template="custom_flatly",
        title="Average Value per Metric (Radar)"
    )

    current_week, pct_change, avg_val, max_val, min_val = kpis
    if pct_change is not None:
        if pct_change < 0:
            summary_text = "🔴 Performance decline in Technology metrics\n"
        else:
            summary_text = "🟢 Technology metrics showing improvement\n"
    else:
        summary_text = "No previous data for comparison.\n"
    summary_text += f"For {category}, average: {avg_val:.2f}, max: {max_val:.2f}, min: {min_val:.2f}."

    return fig, filtered_data.to_dict("records"), kpi_cards, radar_fig, summary_text


# ------------------------------
# Properties Callbacks
# ------------------------------
@app.callback(
    Output("properties-table-collapse", "is_open"),
    Input("properties-table-toggle-btn", "n_clicks"),
    State("properties-table-collapse", "is_open")
)
def toggle_properties_table_collapse(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open

@app.callback(Output("properties-metric-dropdown", "options"), Input("properties-category-dropdown", "value"))
def update_properties_metric_dropdown(category):
    return [{"label": metric, "value": metric} for metric in category_metric_map_properties.get(category, [])] if category else []

@app.callback(
    [
        Output("properties-graph", "figure"),
        Output("properties-data-table", "data"),
        Output("properties-kpi-cards", "children"),
        Output("properties-summary", "children"),
    ],
    [
        Input("properties-category-dropdown", "value"),
        Input("properties-metric-dropdown", "value"),
        Input("properties-date-range-picker", "start_date"),
        Input("properties-date-range-picker", "end_date"),
    ],
)
def update_properties_graph_table_kpis(category, metrics, start_date, end_date):
    if not category or not metrics:
        empty_fig = go.Figure(layout=go.Layout(title="Please select category and metrics to display data", template="custom_flatly"))
        return empty_fig, [], [], ""

    filtered_data = data_properties[
        (data_properties["Category"] == category) &
        (data_properties["Metric"].isin(metrics)) &
        (data_properties["Week Start Date"] >= pd.to_datetime(start_date)) &
        (data_properties["Week Start Date"] <= pd.to_datetime(end_date))
    ]

    if filtered_data.empty:
        empty_fig = go.Figure(layout=go.Layout(title="No Data Available", template="custom_flatly"))
        return empty_fig, [], [], ""

    kpis = calculate_kpis(filtered_data)
    kpi_cards = generate_kpi_cards(kpis)

    filtered_data = filtered_data.sort_values("Week Start Date")
    rolling_window = 4
    filtered_data["Rolling_Avg"] = filtered_data.groupby(["Metric"])["Value"].transform(lambda x: x.rolling(rolling_window, min_periods=1).mean())

    avg_value = filtered_data["Value"].mean()

    fig = px.line(
        filtered_data,
        x="Week Start Date",
        y="Value",
        color="Metric",
        title=f"{category} Metrics (Properties & Investment)",
        markers=True,
        template="custom_flatly",
        hover_data={"Week Start Date": True, "Value": ":.2f", "Metric": True}
    )

    for met, grp in filtered_data.groupby("Metric"):
        fig.add_trace(
            go.Scatter(
                x=grp["Week Start Date"],
                y=grp["Rolling_Avg"],
                mode="lines",
                line=dict(dash="dot", width=2),
                name=f"{met} (Rolling Avg)"
            )
        )

    fig.add_hline(y=avg_value, line_width=2, line_dash="dash", line_color="red")
    fig.add_annotation(
        x=filtered_data["Week Start Date"].iloc[-1],
        y=avg_value,
        text="Overall Avg",
        showarrow=True,
        arrowhead=2,
        ax=0,
        ay=-40,
        font=dict(color="red")
    )

    fig.update_layout(legend_title_text='Metric')
    fig.update_traces(marker=dict(size=6), line=dict(width=2))
    fig.update_layout(transition=dict(duration=500, easing='cubic-in-out'))

    current_week, pct_change, avg_val, max_val, min_val = kpis
    if pct_change is not None:
        if pct_change < 0:
            summary_text = "🔴 Performance decline, corrective action may be needed.\n"
        else:
            summary_text = "🟢 Performance improving, keep it up!\n"
    else:
        summary_text = "No previous data for comparison.\n"

    summary_text += f"\nFor the selected metrics and category ({category}), the average value is {avg_val:.2f}, with a maximum of {max_val:.2f} and minimum of {min_val:.2f}.\n"
    if pct_change is not None:
        summary_text += f"Current performance changed by {pct_change:+.2f}% compared to the previous period."

    return fig, filtered_data.to_dict("records"), kpi_cards, summary_text


if __name__ == "__main__":
    app.run_server(debug=True)
