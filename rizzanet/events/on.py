

def on(func,event):
    '''adds a callable to the global event pool '''
    from flask import g
    from functools import wraps
    @wraps(func)
    def event_wrap(*args,**kwargs):
        return func(*args, **kwargs)
    from eventpool import eventpool
    eventpool.attachEventListener(event, event_wrap)
    return event_wrap
    
