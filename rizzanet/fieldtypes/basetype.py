from abc import ABCMeta, abstractmethod, abstractproperty

class BaseType(metaclass=ABCMeta):
    '''Base type for all type classes'''
    @abstractmethod
    def render(self):
        '''How to render the type'''
        pass
    
    

    @abstractmethod
    def verify(self, instance):
        '''verify the instance of a type'''
        pass
    
    @classmethod
    def get_type_name(cls):
        return cls.type_name
    
    @classmethod
    def set_type_name(cls, name):
        cls.type_name = name

    type_name = abstractproperty(set_type_name, get_type_name)

    def __str__(self):
        self.get_type_name()
    
    def __repr__(self):
        self.get_type_name()
    
    
    
    @classmethod
    def create(cls, data):
        from .valueobject import ValueObject
        return ValueObject(data,cls)
    
    @staticmethod
    def get(data):
        '''method that retrieves data for a given type '''
        return data 
            
