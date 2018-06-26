from abc import ABCMeta, abstractmethod, abstractproperty, abstractclassmethod

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
    
    @abstractclassmethod
    def get_es_mapping(cls):
        '''Gets the elastic search mapping for a given type in the form of a field'''
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
    
    @staticmethod
    def get_es_value(data):
        '''Method that gets the data to be stored in elastic search for a given type'''
        return data
    
    @classmethod
    def get_es_value(cls, data):
        '''Alias of the get method. Passes a value to elastic search that can later be loaded ''' 
        return cls.get(data)
            
