
class CacheItem:
    def __init__(self, pool, key, value, expires = 0):
        self._pool = pool
        self._key = key
        self._value = value
        self._expires = expires
    
    def set_value(self, value):
        self._value = value
    
    def get_value(self):
        return self._value
    
    def set_key(self, value):
        self._value = value

    def store(self):
        return self._pool.set_value(self._key, self._value, self._expires)

    def refresh(self):
        self._value = self._pool.set_value(self._key)
        return self._value

    def set_lifetime(self, val):
        self._expires = val

    def increase_lifetime(self, val):
        self._expires += val
    
    def is_miss(self):
        return self._value == None
    
    def purge(self):
        self._pool.purge(self._key)