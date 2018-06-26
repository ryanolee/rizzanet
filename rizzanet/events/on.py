

def on(event, *listener_args, **listener_kw_args):
    '''adds a callable to the global event pool '''
    def arg_wrapper(func):
        from functools import wraps
        print('called!')
        @wraps(func)
        def event_wrap(*args,**kwargs):
            return func(*listener_args, *args,**listener_kw_args, **kwargs)
        
        from .eventpool import attachEventListener
        attachEventListener(event, event_wrap)
        return event_wrap
    return arg_wrapper
    
