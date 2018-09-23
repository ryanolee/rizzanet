import logging
from rizzanet.core.logging import get_logger, format_var

class GlobalEventPool:
    
    '''Global pool for events '''
    ''' A dictionary of name:[event...]'''
    events = {}

    def __init__(self, eventsPool={}):
        if not all([not isinstance(events ,list) or all([callable(event) for event in events]) for events in eventsPool.values()]):
            raise Exception('Invalid format for events pool')
        self.events = eventsPool

    
    def attachEventListener(self, name, callback):
        '''Attach a new event listener to the event pool'''
        if not callable(callback):
            raise TypeError('Error callback for event {0!s} given as type {1!s}. Expecting callable'.format(name ,type(callback)))
        if not name in self.events.keys():
            self.events[name] = []
        self.events[name].append(callback)

    
    
    def dispatchEvent(self, name, *args, **kwargs):
        '''Dispatch a new event from the event pool'''
        if name in self.events.keys():
            return [event(*args, **kwargs) for event in self.events[name]]
        return []

eventpool = GlobalEventPool()
def getEventPool():
    global eventpool
    return eventpool

def attachEventListener(name, callback):
    '''Attach a new event listener to the event pool'''
    global eventpool
    eventpool.attachEventListener(name, callback)

def dispatchEvent(name, *args, **kwargs):
    '''Dispatch a new event from the event pool'''
    global eventpool
    rizzanet_logger = get_logger()
    if rizzanet_logger.isEnabledFor(logging.DEBUG): rizzanet_logger.debug('Dispatching event {0!s} with args: {1} and kwargs: {2}'.format(name,format_var(args),format_var(kwargs)))
    return eventpool.dispatchEvent(name, *args, **kwargs)