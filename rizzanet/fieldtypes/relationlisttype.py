from .baselisttype import BaseListType
from .relationtype import RelationType

class RelationListType(BaseListType,RelationType):
    item_type = RelationType
