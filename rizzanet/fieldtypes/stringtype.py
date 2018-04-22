
from .basetype import BaseType
class StringType(BaseType):
    '''stringtype for rizzanet'''
    type_name = 'string'
    @classmethod
    def verify(cls, instance):
        return isinstance(instance,str)

    
