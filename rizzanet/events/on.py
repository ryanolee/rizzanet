

def on(event, *listener_args, **listener_kw_args):
    '''adds a callable to the global event pool '''
    def arg_wrapper(func):
        from functools import wraps
        if isinstance(func,staticmethod) or isinstance(func,classmethod):
            func = func.f
        @wraps(func)
        def event_wrap(*args,**kwargs):
            return func(*listener_args, *args,**listener_kw_args, **kwargs)
        
        from .eventpool import attachEventListener
        attachEventListener(event, event_wrap)
        return event_wrap
    return arg_wrapper
    
