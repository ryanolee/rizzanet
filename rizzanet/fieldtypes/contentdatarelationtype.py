
from .relationtype import RelationType
class ContentDataRelationType(RelationType):

    type_name = 'content_data_relation'

    @classmethod
    def verify(cls, instance):
        from rizzanet.models import ContentData
        if not isinstance(instance,int):
            return False
        if not ContentData.exsists(instance):
            return False
        return True

    @staticmethod
    def get(data):
        from rizzanet.models import ContentData
        return ContentData.get_by_id(data)

    
        