from .bundle import bind_js_bundles,bind_css_bundles,get_environment_from_app
from flask import Flask,render_template
from flask_bootstrap import Bootstrap
from rizzanet.admin import bind_admin_routes
from rizzanet.api import bind_api_routes
from .db import init_db
from .cli import bind_cli_commands
from .login import bind_login

import rizzanet.models,rizzanet.views as views,os

def create_app(config=None):
    """creates the app"""
    init_db()
    app = Flask('rizza_app',static_url_path='',static_folder=os.path.dirname(__file__)+"/../static/", template_folder=os.path.dirname(__file__)+"/../templates/")
    bind_bundles(app)
    Bootstrap(app)
    views.register_routes(app)
    bind_cli_commands(app)
    bind_login(app)
    bind_admin_routes(app)
    bind_api_routes(app)
    app.secret_key='123456789'
    return app


def bind_bundles(app):
    """Binds a set of bundles to an app"""
    env=get_environment_from_app(app)
    bind_js_bundles(env)
    bind_css_bundles(env)



app=create_app()


    
