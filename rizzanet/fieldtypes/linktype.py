
from .relationtype import RelationType

class LinkType(RelationType):
    type_name = 'link'
    @staticmethod
    def get(data):
        return RelationType.get(data).get_full_path()
    