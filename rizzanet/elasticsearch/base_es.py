
class BaseES:
    '''The base class for elastic search helpers
    Attributes:
        INDEX_NAME (str): The index name to add mappings to
        es (Elasticsearch): The connection object hte content class will use
    '''
    INDEX_NAME = 'rz_base'

    def __init__(self, conn):
        """
        The helper class for operations on content through elastic search
        Args:
            conn (Elasticsearch): The connection this instance of the content class will use
        """
        self.es=conn
    
    def dropIndex(self):
        '''Drops entire index for elastic search use with caution!'''
        self.es.indices.delete(index=self.INDEX_NAME, ignore=[400, 404])
        return self
    
    def createIndex(self):
        self.es.indices.create(index=self.INDEX_NAME)
