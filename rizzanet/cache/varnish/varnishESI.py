
class VarnishESI:
    def __init__(self, app):
        
    
    def storeESI(self, data, tags, ttl = 3600):
        from rizzanet.cache.keyvalue.cachePool import get_cache_pool
        import json
        from hashlib import md5
        key = md5(data).hexdigest()
        cache_pool = get_cache_pool()
        data = json.dumps({
            'ttl': ttl,
            'data': data,
            'tags': tags
        })
        cache_pool.set_item(key, data, ttl)
    
    def renderESI(self, renderParam, *args, tags=[], **kwargs):
        from rizzanet.core.render import get_render_service
        renderService = get_render_service()
        res = renderService.render()
    
    def loadESI(self, hash):
        from rizzanet.cache.keyvalue.cachePool import get_cache_pool
        import json
        cache_pool = get_cache_pool()
        esiData = cache_pool.get_item()
        if res.is_miss():
            self._loadESIFail(hash)
        from rizzanet

            
    def _loadESIFail(self, hash):
        '''Purge all effected pages if ESI fails to load'''
        from .varnishBanner import get_varnish_banner
        banner = get_varnish_banner()
        return banner.ban_tag(hash)
        
    
    
