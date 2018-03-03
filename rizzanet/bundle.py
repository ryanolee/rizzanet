from flask_assets import Environment, Bundle
import jsmin

def get_environment_from_app(app):
    """Gets environment from Flask app and registers flask_assets
    Args:
        app (Flask): The flask app to bind
    Returns:
        Environment: The new environment
    """
    assets = Environment(app)
    assets.init_app(app)
    return assets
def bind_js_bundles(assets):
    """Binds JS bundles to app
    Args:
        assets (Environment): The current app to bind
    Returns:
        Environment: The new assests set
    """
    
    js = Bundle("js/jquery-3.2.1.slim.min.js",
    "js/popper.min.js",
    "js/bootstrap.min.js",
                filters='jsmin', output='compiled/packed.js')
    assets.register('js_all',js)
    return assets

def bind_css_bundles(assets):
    """Binds css/Scss bundles to app
    Args:
        assets (Environment): The current app to bind
    Returns:
        Environment: The new assests set
    """
    scss = Bundle('sass/core.scss', filters='pyscss')
    css = Bundle(scss,'css/bootstrap.min.css', filters='cssmin', output='compiled/packed.css')
    assets.register('css_all',css)
    return assets