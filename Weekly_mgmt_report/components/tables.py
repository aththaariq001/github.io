from dash import dash_table

def create_data_table(df, table_id):
    return dash_table.DataTable(
        id=table_id,
        columns=[{"name": col, "id": col} for col in df.columns],
        data=[],
        style_table={"overflowX": "auto"},
        style_header={
            "backgroundColor": "#ecf0f1",
            "fontWeight": "bold",
            "color": "#2c3e50",
            "position": "sticky",
            "top": 0,
            "zIndex": 1,
        },
        style_cell={
            "backgroundColor": "#ffffff",
            "color": "#343a40",
            "padding": "0.75rem",
            "textAlign": "center",
            "whiteSpace": "normal",
            "height": "auto",
        },
        style_data_conditional=[
            {"if": {"row_index": "odd"}, "backgroundColor": "#f2f2f2"},
            {
                "if": {"column_id": "Comment"},
                "textAlign": "left",
                "minWidth": "200px",
                "width": "300px",
            },
        ],
        page_size=10,
        sort_action="native",
        filter_action="native",
        row_selectable="multi",
    )
