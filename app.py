# import dash components
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

# import everything else
import flask
import pandas as pd
import os

# initialize the app
server = flask.Flask('app')
server.secret_key = os.environ.get('secret_key', 'secret')
app = dash.Dash('app', server=server)
dcc._js_dist[0]['external_url'] = 'https://cdn.plot.ly/plotly-basic-latest.min.js'

# load data
df = pd.read_csv('meshdash_data_sample.csv')

# create labels for dropdown menu
labels = []
for i in df.node_ip.unique():
    labels.append({'label': i, 'value': i})

# create the main view
app.layout = html.Div([
    html.H1('Mesh Ping Time Delta (mins)'),
    dcc.Dropdown(
        id='node_ip',
        options=labels,
        value=labels[0]['label']
    ),
    dcc.Graph(id='time_delta_min')
], className="container")


# create the graph element
@app.callback(Output('time_delta_min', 'figure'), [Input('node_ip', 'value')])
def update_graph(selected_dropdown_value):
    dff = df[df['node_ip'] == selected_dropdown_value]
    return {
        # make changes to data here
        'data': [{
            'x': dff.timestamp,
            'y': dff.time_delta_min,
            # edit visuals here
            'line': {
                'width': 3,
                'shape': 'linear'
            }
        }],
        # ...and here
        'layout': {
            'margin': {
                'l': 30,
                'r': 20,
                'b': 30,
                't': 20
            }
        }
    }


if __name__ == '__main__':
    app.config.update(TEMPLATES_AUTO_RELOAD=True)
    app.scripts.config.serve_locally = False
    app.run_server(debug=True)
