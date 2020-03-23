import dash_core_components as dcc
import dash_html_components as html
import dash_table

import pandas as pd



def layout(app):
    from app.extensions import db
    from app.models import Portfolio

    with app.app_context():
        query = (db.session.query(Portfolio.travel_product,
                                  db.func.sum(Portfolio.spend_ac).label('spend_ac'),
                                  db.func.sum(Portfolio.bookings_ac).label('bookings_ac'))) \
            .group_by(Portfolio.travel_product).statement
        df = pd.read_sql(query, con = db.session.bind)


    layout  = html.Div([
        html.Div([
            html.H1(children='Portfolio'),
            html.Div(children='Province'),
            dcc.Dropdown(
                id='dropdown',
                options=[
                    {'label': i, 'value': i} for i in df.travel_product.unique()
                ],
                value=None
            ),
            dash_table.DataTable(
                id='table',
                columns=[{"name": i, "id": i} for i in df.columns],
                data=df.to_dict('records'),
            )
        ], className="subpage")
    ], className="page")
    return layout