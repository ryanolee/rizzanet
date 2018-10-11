
from abc import ABCMeta, abstractmethod

class BaseAdapter(ABCMeta):


    '''Gets item from cahce by key'''
    @abstractmethod
    def get_item(self, key):
        pass

    '''Sets an item'''
    @abstractmethod
    def set_item(self, key, value, ttl = 0):
        pass

    '''Sets a mutex on an item in cache'''
    @abstractmethod
    def lock(self, key):
        pass

    '''Purge key'''
    @abstractmethod
    def purge(self, key):
        pass

    def get_items(self, keys):
        return { key: self.get_item(key) for key in keys}


    '''sets a number of items'''
    def set_items(self, keyvaldict):
        return [self.set_item(key,value) for key, value in self.key]

