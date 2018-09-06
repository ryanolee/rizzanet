from .baselisttype import BaseListType
from .contentdatarelationtype import ContentDataRelationType

class ContentDataRelationListType(BaseListType, ContentDataRelationType):
    item_type = ContentDataRelationType

    @classmethod
    def get_es_mapping(cls):
        return {"type":  "keyword"}

    @staticmethod
    def get_es_value(data):
        return ','.join([str(item) for item in data])
    
    @staticmethod
    def get(data):
        from rizzanet.models import ContentData
        return ContentData.get_by_ids(data)
