
from .baseAdapter import BaseAdapter
from redis import Redis
from rizzanet.core.logging import get_logger

class RedisAdapter(BaseAdapter):
    def __init__(self, app):
        self._conn = Redis(**app.config['REDIS'])

    def set_item(self, key, value, ttl = 0):
        rz_log = get_logger()
        try:
            rz_log.debug('Setting cache item {0}'.format(key))
            self._conn.set(key, value, ttl)
            return True
        except Exception as error:
            rz_log.error('Connot cache variable {0} in redis. Error message {1!s}'.format(key, error.message))
            return False
        
    def get_item(self, key):
        rz_log = get_logger()
        try:
            rz_log.debug('Getting cache item {0}'.format(key))
            return self._conn.get(key)
        except Exception as error:
            rz_log.error('Connot cache variable {0} in redis. Error message {1!s}'.format(key, error.message))
            return False
        

