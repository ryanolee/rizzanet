
from rizzanet.events import attachEventListener
from .content_es import ContentES
from .content_type_es import ContentTypeES
from .connection import getConnectionFromApp

def bind_es_events(app):
    '''Bind elastic search event listeners to global event pool'''
    #Bind content event listenters
    conn = getConnectionFromApp(app)
    content = ContentES(conn)
    content_type = ContentTypeES(conn)
    attachEventListener('CREATE_CONTENT', content.addToIndex)
    attachEventListener('CREATE_CONTENT_TYPE', content_type.createIndexFromType)