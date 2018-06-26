

from .base_es import BaseES
from elasticsearch import Elasticsearch, helpers
'''The elasticsearch helper content class'''
class ContentES(BaseES):

    MAPPING = {
        'content': {
            'dynamic': 'strict',
            'properties': {
                'id': {'type': 'integer'},
                'parent_id': {'type': 'integer'},
                'name': {'type':'text', 'analyzer': 'english'},
                'remote_id': {'type':'keyword'},
                'content_type_id': {'type': 'integer'},
                'content_data_id': {'type': 'integer'}
            }
        }
    }

    INDEX_NAME = 'rz_content'

    MAPPING_NAME = 'content'

    def createMapping(self):
        self.es.indices.put_mapping(index=self.INDEX_NAME, doc_type=self.MAPPING_NAME, body=self.MAPPING)
    
    def addToIndex(self, content):
        from rizzanet.models import Content
        if not isinstance(content, Content):
            raise ValueError('Error expecting content class. Got '+type(content))
        self.es.index(index=self.INDEX_NAME, doc_type=self.MAPPING_NAME, id=content.id, body=content.as_dict())

    def reindex(self):
        '''Reindexes all entries of content type. It does this in a bulk action'''
        from rizzanet.models import Content
        self.dropIndex()
        self.createIndex()
        self.createMapping()
        actions =({
            '_op_type': 'index',
            '_index': self.INDEX_NAME,
            '_type': self.MAPPING_NAME,
            '_id': content.id,
            **content.as_dict()
        } for content in Content.all())
        helpers.bulk(self.es, actions)
    
    

