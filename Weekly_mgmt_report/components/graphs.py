from dash import dcc
import plotly.graph_objects as go

def create_graph(graph_id, title=""):
    return dcc.Graph(id=graph_id, figure=go.Figure(layout=go.Layout(title=title, template="custom_flatly")))
