

class ValueObject():
    def __init__(self,data,TypeClass):
        from .basetype import BaseType 
        if not issubclass(TypeClass,BaseType):
            raise TypeError('Class {0} does not inherit from BaseType'.format(TypeClass))
        if not TypeClass.verify(data):
            raise ValueError('Cannot instanchiate value object supplied data is invalid. Type: {0} Value: {1}'.format(TypeClass, data))
        self.type = TypeClass
        self._data = data
    
    def render(self):
        return self.type.render(self)

    
    def get(self):
        return self.type.get(self._data)
    
    def get_es_value(self):
        return self.type.get_es_value(self._data)
    
    def __getattr__(self, name):
        if name in dir(self):
            return getattr(self, name)
        method = getattr(self.type, name, None)
        if callable(method):
            return lambda *args,**kwargs: method(self,*args,**kwargs)
        raise AttributeError("Neither {0!r} or {1!r} has method {2}".format(self._type, self.__class__, name))
    
    def __setstate__(self, data):
        from .alltype import CLASS_MAPPINGS
        self.type = CLASS_MAPPINGS[data['t']]
        self._data = data['d']
    
    def __getstate__(self):
        from .alltype import CLASS_MAPPINGS
        for key, val in CLASS_MAPPINGS.items():
            if val == self.type:
                mapping = key

        return {
            't':mapping,
            'd':self._data
            }
    
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, key):
        if not self.is_list_type():
            raise TypeError('{0!r} is not subscriptable')
        return self._data[key]
    
    def __setitem__(self, key, value):
        if not self.is_list_type():
            raise TypeError('{0!r} is not subscriptable')
        if not self.type.verify_item(value):
            raise TypeError('{0!r} is not a valid item of self {1!r}'.format(value, self.type))
        self._data[key] = self.type.set_item(value)
    
    def __iter__(self):
        try: iter(self._data)
        except: raise TypeError("{0!r} is not iterable".format(self.type))
        if self.is_list_type():
            return (self.type.get_item(item) for item in self._data)
        return self._data
    
    def __repr__(self):
        return "<ValueObject({0})>".format(self.get())
    
    def is_list_type(self):
        from .baselisttype import BaseListType
        return issubclass(self.type, BaseListType)