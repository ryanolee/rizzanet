
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
    
    @classmethod
    def convert(cls, data):
        if isinstance(data, str):
            try: return int(data)
            except ValueError: return data
        return data
    
    @staticmethod
    def get_es_value(data):
        return data

    @staticmethod
    def get(content_object_id):
        from rizzanet.models import Content
        return Content.get_by_id(content_object_id)

    
        