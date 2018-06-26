

from .base_es import BaseES
from elasticsearch import Elasticsearch, helpers

'''The elasticsearch helper content class'''
class ContentDataES(BaseES):

    INDEX_NAME = None

    def reindex(self):
        from rizzanet.models import ContentData, ContentType
        from .content_type_es import ContentTypeES
        #Reindex content types to get new set of mappings then index content data
        content_type_es = ContentTypeES(self.es)
        content_type_es.reindex()
        #create a list of genartors for each content data type
        all_data = [ContentData.all(content_type) for content_type in ContentType.all()]

        def inturnal_iterator(all_data):
            for data_list in all_data:
                for data in data_list:
                    yield data

        actions =({
            '_op_type': 'index',
            '_index': content_type_es.INDEX_NAME+content_data.get_datatype(),
            '_type': content_data.get_datatype(),
            '_id': content_data.id,
            **{key: value.get_es_value() for key, value in content_data.get_data_dict().items()}
        } for content_data in inturnal_iterator(all_data) )
        
        helpers.bulk(self.es, actions)
