from .stringtype import StringType
from .relationtype import RelationType
from .linktype import LinkType
from .relationlisttype import RelationListType


'''Class mppings used to optimize storage of attributes'''
CLASS_MAPPINGS = {
    'str':StringType,
    'rel':RelationType,
    'rells':RelationListType,
    'lnk':LinkType
}

__all__ = ['StringType','RelationType','LinkType']