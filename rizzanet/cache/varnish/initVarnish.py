
from .bindVarnishEvents import bind_varnish_events

def init_varnish(app):

    if not app.config['VARNISH_CONFIG']['VARNISH_ENABLED']:
        return False
    
    bind_varnish_events(app)
    
