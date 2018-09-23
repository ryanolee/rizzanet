from .bundle import bind_js_bundles,bind_css_bundles,get_environment_from_app
from flask import Flask,render_template
from flask_bootstrap import Bootstrap
from rizzanet.admin import bind_admin_routes
from rizzanet.api import init as init_api
from rizzanet.views import bind_jinja2_functions,register_routes
from rizzanet.config import BaseConfig
from rizzanet.elasticsearch import bind_es_events
from rizzanet.cache.varnish import init_varnish
from rizzanet.core.logging import init_logger
from .db import bind_app_events
from .cli import bind_cli_commands
from .login import bind_login
from .routing import bind_converters_to_app


import os

def create_app(config=None):
    """creates the app"""
    app = Flask('rizza_app',static_url_path='/static',static_folder=os.path.dirname(__file__)+"/../static/", template_folder=os.path.dirname(__file__)+"/../templates/")
    app.config.from_object(BaseConfig)
    init_logger(app)
    bind_converters_to_app(app)
    bind_bundles(app)
    Bootstrap(app)
    bind_cli_commands(app)
    bind_login(app)
    bind_admin_routes(app)
    init_api(app)
    init_varnish(app)
    bind_app_events(app)
    bind_jinja2_functions(app)
    bind_es_events(app)
    register_routes(app)
    app.secret_key='123456789'
    return app


def bind_bundles(app):
    """Binds a set of bundles to an app"""
    env=get_environment_from_app(app)
    bind_js_bundles(env)
    bind_css_bundles(env)



app=create_app()


    
