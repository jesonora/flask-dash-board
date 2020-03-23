import dash
import geopandas as gpd
import plotly.express as px
import pandas as pd
from shapely import wkt

def register_callbacks(dashapp):
    from app.extensions import db
    from app.models import GeoData

    with dashapp.server.app_context():
        query = db.session.query(GeoData).statement
        df = pd.read_sql(sql=query, con=db.session.bind)

    df['geometry'] = df['geometry'].apply(wkt.loads)
    map_data = gpd.GeoDataFrame(df, geometry='geometry')

    @dashapp.callback(
        dash.dependencies.Output('dropdown-prov', 'options'),
        [dash.dependencies.Input('dropdown-com', 'value')])
    def update_output_prov(value):
        if value not in ['Spain', None]:
            df_prov = map_data[map_data.name_1 == value]
            return [{'label': i, 'value': i} for i in df_prov.name_2.unique()]

        if value  in [None]:
            return {'label': '', 'value': None}

        else:
            df_prov = map_data
            return [{'label': i, 'value': i} for i in df_prov.name_2.unique()]
    @dashapp.callback(
        dash.dependencies.Output('dropdown-prov', 'disabled'),
        [dash.dependencies.Input('dropdown-com', 'value')])
    def drop_enable(value):
        if value not in ['Spain', None]:
            return False
        else:
            return True

    @dashapp.callback(
        dash.dependencies.Output('graph', 'figure'),
        [dash.dependencies.Input('dropdown-prov', 'value'),
         dash.dependencies.Input('dropdown-com', 'value')])
    def update_map(dropdown_prov, dropdown_com):

        print(dropdown_prov, dropdown_com)

        if dropdown_com is not None and dropdown_com != 'Spain' and dropdown_prov in ['Spain', None]:
            df_drop = map_data[map_data.name_1 == dropdown_com]
        elif dropdown_prov is not None and dropdown_prov != 'Spain' and dropdown_com is not None:
            df_drop = map_data[map_data.name_2 == dropdown_prov]
        else:
            df_drop = map_data

        fig = px.choropleth(df_drop, geojson=df_drop, color="nat2018",
                            locations="name_2", featureidkey="properties.name_2",
                            projection="mercator"
                            )
        fig.update_geos(visible=False, fitbounds='geojson')
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0},
                          coloraxis_showscale=False, width=900, height=500)
        return fig

