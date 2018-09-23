
from functools import wraps

def in_app_context(func):
    '''Binds the getter context to a request'''
    def param_validator_decorator(getterClass):
        @wraps(func)
        def real_wrapper(*args, **kwargs):
            from flask import has_request_context, g
            func_name = func.__name__
            if not has_request_context():
                from rizzanet.core.logging import get_logger
                rz_log = get_logger()
                rz_log.error('Tried to get variable outside of the context of the request in call to {0!r}'.format(func_name))
            if not hasattr(g, 'rizzanet_globals'):
                g.rizzanet_globals = {}
            if not func_name in g.rizzanet_globals:
                g.rizzanet_globals[func_name] = getterClass()
            targetInstance = g.rizzanet_globals[func_name] 
            return func(targetInstance ,*args, **kwargs)
        return real_wrapper
    return param_validator_decorator

