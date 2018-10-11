
from .adapters import BaseAdapter
from .cacheItem import CacheItem
from rizzanet.core.logging import get_logger
class CachePool:
    def __init__(self, adapter):
        if not isinstance(adapter, BaseAdapter):
            raise ValueError('Error cannot initialise cache pool class {0!r} does not implement {1!r}'.format(type(adapter), BaseAdapter.__class__))
        self._adapter = adapter
    
    def get_item(self, key):
        value = self._adapter.get_item(key)
        return CacheItem(self, key, value)
    
    def set_item(self, key, value, ttl = 0):
        if not isinstance(str, value):
            rz_log = get_logger()
            rz_log.warn('Unable to store item of type {0!r}'.format(type(value)))
            return None
        self._adapter.set_item(key, value, ttl)
        return CacheItem(self._adapter, key, value, ttl)

    def lock(self, key):
        self._adapter.lock(key)

    def purge(self, key):
        self._adapter.purge(key)

cache_pool = None

def initialise_cace_pool(app):
    global cache_pool
    cache_type = app.config['CACHE_TYPE']
    if cache_pool == 'REDIS':
        from .adapters import RedisAdapter
        cache_pool = CachePool(RedisAdapter(app))
        return cache_pool
    else:
        return NotImplementedError('Error cache type {0} not yet implemented'.format(cache_type))

def get_cache_pool():
    global cache_pool
    return cache_pool

    