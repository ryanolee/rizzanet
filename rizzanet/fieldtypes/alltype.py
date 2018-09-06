from .stringtype import StringType
from .relationtype import RelationType
from .linktype import LinkType
from .contentdatarelationtype import ContentDataRelationType
from .contentdatarelationlisttype import ContentDataRelationListType
from .imagetype import ImageType

'''Class mppings used to optimize storage of attributes'''
CLASS_MAPPINGS = {
    'str':StringType,
    'rel':RelationType,
    'crel':ContentDataRelationType,
    'crells':ContentDataRelationListType,
    'lnk':LinkType,
    'img': ImageType
}

__all__ = ['StringType','RelationType','LinkType','ContentDataRelationType','ContentDataRelationListType','ImageType']