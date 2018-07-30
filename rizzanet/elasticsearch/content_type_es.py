from .base_es import BaseES
from rizzanet.models import ContentType
from elasticsearch import helpers
class ContentTypeES(BaseES):
    
    INDEX_NAME = 'rz_t_'

    def createIndexFromType(self, content_type):
        from rizzanet.models import ContentType
        if not isinstance(content_type, ContentType):
            raise ValueError('Error expecting contentType class. Got '+type(ContentType))
        mapping ={
            'mappings':{
                content_type.get_name(): {
                    'dynamic': 'strict',
                    'properties': {name: field.get_es_mapping() for name,field in content_type.get_schema().items()}
                }
            }
        }
        self.es.indices.create(index = self.INDEX_NAME+content_type.get_name(), body = mapping, ignore=[400, 404])
    def createIndexes(self):
        for content_type in ContentType.all():
            self.createIndexFromType(content_type)

    def dropIndexes(self):
        for index in self.es.indices.get(self.INDEX_NAME + '*'):
            self.es.indices.delete(index=index, ignore=[400, 404])
        
    def reindex(self):
        self.dropIndexes()
        self.createIndexes()
        