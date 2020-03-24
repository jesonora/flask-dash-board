import dash
import pandas as pd


def register_callbacks(dashapp):
    from app.extensions import db
    from app.models import Portfolio

    with dashapp.server.app_context():
        query = (db.session.query(Portfolio.travel_product,
                                  Portfolio.year,
                                  db.func.sum(Portfolio.spend_ac).label('spend_ac'),
                                  db.func.sum(Portfolio.bookings_ac).label('bookings_ac'))) \
            .group_by(Portfolio.travel_product, Portfolio.year).statement
        df = pd.read_sql(query, con=db.session.bind)

    @dashapp.callback(
        dash.dependencies.Output('table', 'data'),
        [dash.dependencies.Input('dropdown', 'value')])
    def update_output(value):
        if value is None:
            df_out = df
            return df_out.to_dict('records')
        else:
            df_out = df[df.travel_product == value]
            return df_out.to_dict('records')




