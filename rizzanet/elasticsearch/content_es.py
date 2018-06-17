
from rizzanet.events.on import on 
from .base_es import BaseES
from elasticsearch import Elasticsearch
'''The elasticsearch helper content class'''
class ContentES(BaseES):

    MAPPING = {
        'content': {
            'dynamic': 'strict',
            'properties': {
                'id': {'type': 'integer'},
                'name': {'type':'string', 'analyzer': 'english'},
                ''
            }
        }
    }

    INDEX_NAME = 'rz_content'

    MAPPING_NAME = 'content'

    def createMapping(self):
        self.es.indices.put_mapping(index=self.INDEX_NAME, doctype=self.MAPPING_NAME)



