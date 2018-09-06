

class ValueObject():
    def __init__(self,data,TypeClass):
        from .basetype import BaseType 
        if not issubclass(TypeClass,BaseType):
            raise TypeError('Class {0} does not inherit from BaseType'.format(TypeClass))
        data = TypeClass.convert(data)
        if not TypeClass.verify(data):
            raise ValueError('Cannot instanchiate value object supplied data is invalid. Type: {0} Value: {1}'.format(TypeClass, data))
        data = TypeClass.after_validation_convert(data)
        
        self.type = TypeClass
        self._data = data
        self._bound_content_data = None
    
    def render(self):
        return self.type.render(self)

    def store(self):
        if self._bound_content_data == None:
            return False
        return self._bound_content_data.update_attr(self)
    
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
        raise AttributeError("Neither {0!r} or {1!r} has method {2}".format(type(self.type), type(self), name))
    
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
    
    def bind_content_data(self, data):
        from rizzanet.models.content_data import ContentData
        if data == self._bound_content_data:
            return
        if not isinstance(data, ContentData):
            raise ValueError('Error: expected an instance of the ContentData class. Got:' + type(data))
        if self._bound_content_data != None:
            raise RuntimeWarning('Warning: ValueObject bound twice. This is not intended behaivour. Original:{0!r} New:{1!r}'.format(self._bound_content_data, data))
        self._bound_content_data = data
        return self
        