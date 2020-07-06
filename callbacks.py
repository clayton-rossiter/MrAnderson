from dash.dependencies import Input, Output
import plotly.graph_objects as go
import dash_core_components as dcc
import numpy as np

from app import app

# @app.callback(
#     Output('app-1-display-value', 'children'),
#     [Input('app-1-dropdown', 'value')])
# def display_value(value):
#     return 'You have selected "{}"'.format(value)

# @app.callback(
#     Output('app-2-display-value', 'children'),
#     [Input('app-2-dropdown', 'value')])
# def display_value(value):
#     return 'You have selected "{}"'.format(value)

@app.callback(
    Output('graph_main','children'),
    [
        Input('textinput_hashtag','value')
    ]
)
def check_hashtag(hashtag):
    # print(hashtag)
    if hashtag != None:
        x = np.arange(10)

        fig = go.Figure(
            data=go.Scatter(
                x=x, y=x**2
            )
        )
        return dcc.Graph(figure=fig)
    else:
        return dcc.Graph()
