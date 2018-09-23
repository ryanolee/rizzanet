
from rizzanet.events import attachEventListener
from rizzanet.cache.varnish import get_varnish_tagger,get_varnish_banner

def bind_varnish_events(app):
    
    tagger = get_varnish_tagger()
    banner = get_varnish_banner(app)

    @app.after_request
    def post_request_tag(response):
        return tagger.add_headers_to_response(response)

    attachEventListener('PUSHED_RENDER_CONTEXT', tagger.tag_node)
    attachEventListener('UPDATE_NODE', banner.ban_node)
        
    
    