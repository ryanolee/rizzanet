
def getConnectionFromApp(app):
    '''Creates an elastic search connection from the config stored in app object'''
    from elasticsearch import Elasticsearch
    return Elasticsearch(app.config['ES_CONFIG'])