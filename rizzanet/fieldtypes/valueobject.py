

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
    
    def __getattr__(self, name):
        if name in dir(self):
            return getattr(self, name)
        method = getattr(self.type, name, None)
        if callable(method):
            return lambda *args,**kwargs: method(self,*args,**kwargs)
        raise AttributeError("Neither {0!r} or {1!r} has method {2}".format(self._type, self.__class__, name))
    
    def __setstate__(self, data):
        self.type = data['t']
        self._data = data['d']
    
    def __getstate__(self):
        return {
            't':self.type,
            'd':self._data
            }