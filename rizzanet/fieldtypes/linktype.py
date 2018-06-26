
from .relationtype import RelationType

class LinkType(RelationType):
    type_name = 'link'

    @classmethod
    def get_es_value(cls, data):
        return cls.get(data)
    
    @staticmethod
    def get(data):
        return RelationType.get(data).get_full_path()
    
    @classmethod
    def get_es_mapping(cls):
        return {'type': 'text', 'analyzer': 'english'}
    