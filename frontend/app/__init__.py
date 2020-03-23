import dash
from flask import Flask
from flask.helpers import get_root_path
from .config import BaseConfig
from .models import User, Portfolio, GeoData


def create_app():
    server = Flask(__name__)
    server.config.from_object(BaseConfig)

    register_extensions(server)
    register_blueprints(server)

    from app.dashapp1.layout import layout as layout1
    from app.dashapp1.callbacks import register_callbacks as register_callbacks1
    register_dashapp(server, 'Dashapp 1', 'dashboard', layout1, register_callbacks1)

    from app.dashapp2.layout import layout as layout2
    from app.dashapp2.callbacks import register_callbacks as register_callbacks2
    register_dashapp(server, 'Dashapp 2', 'graph', layout2, register_callbacks2)

    from app.dashapp3.layout import layout as layout3
    from app.dashapp3.callbacks import register_callbacks as register_callbacks3
    register_dashapp(server, 'Dashapp 3', 'map', layout3(server), register_callbacks3)

    return server

def register_dashapp(app, title, base_pathname, layout, register_callbacks_fun, css_sheet=None):
    # Meta tags for viewport responsiveness
    meta_viewport = {"name": "viewport", "content": "width=device-width, initial-scale=1, shrink-to-fit=no"}

    my_dashapp = dash.Dash(__name__,
                           server=app,
                           url_base_pathname=f'/{base_pathname}/',
                           assets_folder=get_root_path(__name__) + f'/{base_pathname}/assets/',
                           meta_tags=[meta_viewport],
                           external_stylesheets=css_sheet)

    with app.app_context():
            my_dashapp.title = title
            my_dashapp.layout = layout
            register_callbacks_fun(my_dashapp)

def register_extensions(server):
    from app.extensions import db
    from app.extensions import migrate

    db.init_app(server)
    migrate.init_app(server, db)


def register_blueprints(server):
    from app.webapp import server_bp

    server.register_blueprint(server_bp)
