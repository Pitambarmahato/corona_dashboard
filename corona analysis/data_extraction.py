import requests
import dash
import dash_core_components as dcc
import dash_html_components as html
import json
import sys
import pandas as pd
# import matplotlib.pyplot as plt
import dash_core_components
print(dash_core_components.__version__)
response = requests.get("https://corona.lmao.ninja/countries")
# print(response.status_code)

response_data = response.json()
df = pd.DataFrame.from_dict(response_data)
df.to_csv('corona_data.csv')
df_corona = pd.read_csv('corona_data.csv')

def generate_table(dataframe, max_rows = 100):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ])
            for i in range(min(len(dataframe), max_rows))
        ])
    ])

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets = external_stylesheets)
app.layout = html.Div(children=[
    html.H4(children= 'Corona Virus Data (2020)'),
    generate_table(df)
])

# dcc.Graph(
#         id='example-graph',
#         figure={
#             'data': [
#                 {df['country'], 'type': 'bar', 'name': 'SF'},
#                 {df['deaths'], 'type': 'bar', 'name': u'Montréal'},
#             ],
#             'layout': {
#                 'title': 'Dash Data Visualization'
#             }
#         }
#     )
app.layout = html.Div([
    dcc.Graph(
        id='total cases vs total recovered',
        figure={
            'data': [
                dict(
                    x=df[df['country'] == i]['cases'],
                    y=df[df['country'] == i]['recovered'],
                    text=df[df['country'] == i]['country'],
                    mode='markers',
                    opacity=0.7,
                    marker={
                        'size': 10,
                        'line': {'width': 0.5, 'color': 'white'}
                    },
                    name=i
                ) for i in df.country.unique()
            ],
            'layout': dict(
                xaxis={'type': 'log', 'title': 'Total Cases'},
                yaxis={'title': 'Totoal Recovered'},
                margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                legend={'x': 0, 'y': 1},
                hovermode='closest'
            )
        }
    )
])


if __name__ == '__main__':
    app.run_server(debug=True)