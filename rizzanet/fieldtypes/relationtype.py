
from .basetype import BaseType
class RelationType(BaseType):

    type_name = 'relation'

    @classmethod
    def verify(cls, instance):
        from rizzanet.models import Content
        if not isinstance(instance,int):
            return False
        if not Content.exsists(instance):
            return False
        return True
    
    @classmethod
    def get_es_mapping(cls):
        return {'type': 'integer'}
    
    @staticmethod
    def get_es_value(data):
        return data

    @staticmethod
    def get(data):
        from rizzanet.models import Content
        return Content.get_by_id(data)

    
        