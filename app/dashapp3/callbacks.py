import dash
import geopandas as gpd
import json
import plotly.express as px

natalidad = "/Users/jesussono/PycharmProjects/flask-dash-board/data/natalidad.geojson"
map_data = gpd.read_file(natalidad)

with open("/Users/jesussono/PycharmProjects/flask-dash-board/data/natalidad2.geojson") as f:
    data = json.load(f)

def register_callbacks(dashapp):
    @dashapp.callback(
        dash.dependencies.Output('dropdown-prov', 'options'),
        [dash.dependencies.Input('dropdown-com', 'value')])
    def update_output_prov(value):
        if value not in ['Spain', None]:
            df_prov = map_data[map_data.NAME_1 == value]
            return [{'label': i, 'value': i} for i in df_prov.NAME_2.unique()]

        if value  in [None]:
            return {'label': '', 'value': None}

        else:
            df_prov = map_data
            return [{'label': i, 'value': i} for i in df_prov.NAME_2.unique()]
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
            df_drop = map_data[map_data.NAME_1 == dropdown_com]
        elif dropdown_prov is not None and dropdown_prov != 'Spain' and dropdown_com is not None:
            df_drop = map_data[map_data.NAME_2 == dropdown_prov]
        else:
            df_drop = map_data

        fig = px.choropleth(df_drop, geojson=data, color="NAT2018",
                            locations="NAME_2", featureidkey="properties.NAME_2",
                            projection="mercator"
                            )
        fig.update_geos(visible=False, fitbounds='geojson')
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0},
                          coloraxis_showscale=False, width=900, height=500)
        return fig

