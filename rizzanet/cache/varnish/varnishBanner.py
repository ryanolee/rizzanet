from urllib import parse, request

class VarnishBanner():
    VARNSIH_BAN_HEADER = 'X-rizzanet-ban-tags'

    def __init__(self, app):
        config = app.config['VARNISH_CONFIG']
        self.purge_servers = config['VARNISH_PURGE_SERVER_HOSTS']
        if isinstance(self.purge_servers, str):
            if ',' in self.purge_servers:
                self.purge_servers= self.purge_servers.split(',')
            else:
                self.purge_servers = [self.purge_servers]
    
    def ban_node(self, node):
        from .varnishTagger import VarnishTagger
        tagger = VarnishTagger()
        node_to_ban = tagger.get_tag_for_node(node)
        return self._do_ban(node_to_ban)

    def ban_tag(self, tag):
        return self._do_ban(tag) 
    
    def _do_ban(self, header_value):
        from http.client import HTTPConnection
        
        from rizzanet.core.logging import get_logger, format_var
        rz_log = get_logger()
        for host in self.purge_servers:
            rz_log.debug('Banning varnish for tags: {0}'.format(header_value))
            conn = HTTPConnection(host)
            try:
                conn.request('BAN','/',headers={
                    self.VARNSIH_BAN_HEADER: header_value
                })
                res = conn.getresponse()
                data = res.read()
                conn.close()
                rz_log.debug('Purged varnish with code {0}'.format(res.code))
            except Exception as error:
                rz_log.error('Connot purge item from varnish. Reason {0!s}'.format(error))
            
def get_varnish_banner(app):
    return VarnishBanner(app)