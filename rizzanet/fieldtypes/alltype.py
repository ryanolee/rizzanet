from .stringtype import StringType
from .relationtype import RelationType
from .linktype import LinkType


'''Class mppings used to optimize storage of attributes'''
CLASS_MAPPINGS = {
    'str':StringType,
    'rel':RelationType,
    'lnk':LinkType
}

__all__ = ['StringType','RelationType','LinkType']