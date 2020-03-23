import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import geopandas as gpd

import pandas as pd
from shapely import wkt


def layout(app):
    from app.extensions import db
    from app.models import GeoData

    with app.app_context():
        query = db.session.query(GeoData).statement
        df = pd.read_sql(sql = query, con = db.session.bind)

    df['geometry'] = df['geometry'].apply(wkt.loads)
    map_data = gpd.GeoDataFrame(df, geometry='geometry')

    fig = px.choropleth(map_data, geojson=map_data, color="nat2018",
                        locations="name_2", featureidkey="properties.name_2",
                        projection="mercator"
                       )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, coloraxis_showscale=False)


    layout  = html.Div([
        html.Div([
            html.H1(children='Natality in Spain'),
            html.Div(children='Community'),
            dcc.Dropdown(
                id='dropdown-com',
                options=[
                    {'label': i, 'value': i} for i in map_data.name_1.unique()
                ],
                value='Spain'
            ),
            html.Div(children='Province'),
            dcc.Dropdown(
                id='dropdown-prov',
                options=[
                    {'label': i, 'value': i} for i in map_data.name_2.unique()
                ],
                value='Spain',
                disabled=True
            ),

            dcc.Graph(id='graph',
                      figure=fig)
        ], className="subpage")
    ], className="page")
    return layout