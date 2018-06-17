
class GlobalEventPool:
    
    '''Global pool for events '''
    ''' A dictionary of name:[event...]'''
    events = {}

    def __init__(self, eventsPool={}):
        if not all([not isinstance(events ,list) or all([callable(event) for event in events]) for events in eventsPool.values()]):
            raise Exception('Invalid format for events pool')
        self.events = eventsPool

    '''Attach a new event listener to the event pool'''
    def attachEventListener(self, name, callback):
        if not callable(callback):
            raise TypeError('Error callback for event {0!s} given as type {1!s}. Expecting callable'.format(name ,type(callback)))
        if not name in self.events.keys():
            self.events[name] = []
        self.events[name].append(callback)
    
    '''Dispatch a new event from the event pool'''
    def dispatchEvent(self, name, *args, **kwargs):
        if name in self.events.keys():
            return [event(*args, **kwargs) for event in self.events[name]]
        return []
global eventpool
eventpool = GlobalEventPool()
