
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
    
    @staticmethod
    def get(data):
        from rizzanet.models import Content
        return Content.get_by_id(data)
        