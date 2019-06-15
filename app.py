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
df_wifi = pd.read_csv('meshdash_data_wifi.csv')
df_ping = pd.read_csv('meshdash_data_ping.csv')
# create labels for dropdown menu
labels = []
for i in df.node_ip.unique():
    labels.append({'label': i, 'value': i})

# create the main view
app.layout = html.Div([

    # selector
    dcc.Dropdown(id='node_ip', options=labels, value=labels[0]['label']),

    # first plot
    html.H1('Node Downtime (mins)'),
    dcc.Graph(id='node_downtime_min'),

    # second plot
    html.H1('Number of Connections'),
    dcc.Graph(id='active_connections'),

    # third plot
    html.H1('Max Ping (ms)'),
    dcc.Graph(id='max_ping'),

    # visuals ends here
], className="container")


# create the graph element
@app.callback(Output('node_downtime_min', 'figure'), [Input('node_ip', 'value')])
def node_downtime_min(selected_dropdown_value):
    data = df[df['node_ip'] == selected_dropdown_value]
    return {
        # make changes to data here
        'data': [{
            'x': data.timestamp,
            'y': data.time_delta_min,
            # edit visuals here
            'line': {
                'width': 2,
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


# create the graph element
@app.callback(Output('active_connections', 'figure'), [Input('node_ip', 'value')])
def active_connections(selected_dropdown_value):
    data = df_wifi[df_wifi['node_ip'] == selected_dropdown_value]
    return {
        # make changes to data here
        'data': [{
            'x': data.timestamp,
            'y': data.no_of_connections,
            # edit visuals here
            'line': {
                'color': 'rgb(231,107,243)',
                'width': .3,
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


@app.callback(Output('max_ping', 'figure'), [Input('node_ip', 'value')])
def ping_delta(selected_dropdown_value):
    data = df_ping[df_ping['node_ip'] == selected_dropdown_value]
    return {
        'data': [{
            'y': data['max'],
            'x': data.timestamp,
            'line': {
                'color': 'rgb(255,99,71)',
                'width': .3,
                'shape': 'linear'
            }
        }],
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
