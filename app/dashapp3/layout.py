import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import geopandas as gpd
import json


natalidad = "/Users/jesussono/PycharmProjects/flask-dash-board/data/natalidad.geojson"
map_data = gpd.read_file(natalidad)

with open("/Users/jesussono/PycharmProjects/flask-dash-board/data/natalidad2.geojson") as f:
    data = json.load(f)


fig = px.choropleth(map_data, geojson=data, color="NAT2018",
                    locations="NAME_2", featureidkey="properties.NAME_2",
                    projection="mercator", width=700, height=500
                   )
fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, coloraxis_showscale=False)


layout  = html.Div([
    html.H1(children='Natality in Spain'),
    html.Div(children='Community'),
    dcc.Dropdown(
        id='dropdown-com',
        options=[
            {'label': i, 'value': i} for i in map_data.NAME_1.unique()
        ],
        value='Spain'
    ),
    html.Div(children='Province'),
    dcc.Dropdown(
        id='dropdown-prov',
        options=[
            {'label': i, 'value': i} for i in map_data.NAME_2.unique()
        ],
        value='Spain',
        disabled=True
    ),

    dcc.Graph(id='graph', figure=fig)
])