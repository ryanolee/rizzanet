
class RequestContextProvider:

    def __init__(self, target_class):
        self.__dict__['target_class'] = target_class
    
    def __getattr__(self, name):
        
        proxy_instance = self.__dict__['target_class']()

        if hasattr(proxy_instance, name) and callable(getattr(proxy_instance, name)):
            return UnboundClassMethod(self, name)


        instance = self._get_instance()
        if not hasattr(instance, name):
            raise AttributeError('{0!r} has no attribute {1}'.format(instance, name))
        return getattr(instance, name)

    def __setattr__(self, name, value):
        instance = self._get_instance()
        setattr(instance, name, value)

    def _get_instance(self):
        from flask import has_request_context, g
        from rizzanet.core.logging import get_logger
        if not has_request_context():
            from rizzanet.core.logging import get_logger
            rz_log = get_logger()
            rz_log.error('Tried to get variable outside of the context of the request in call to')
        if not hasattr(g, 'rizzanet_request_context'):
            g.rizzanet_request_context = {}
        class_name = self.__dict__['target_class'].__name__
        if not class_name in g.rizzanet_request_context:
            g.rizzanet_request_context[class_name] = self.__dict__['target_class']()
        return g.rizzanet_request_context[class_name]

class UnboundClassMethod():
    def __init__(self, bound_instance, name):
        self.bound_instance = bound_instance
        self.name = name
    
    def __call__(self, *args, **kwargs):
        instance = self.bound_instance._get_instance()
        method = getattr(instance, self.name)
        return method(*args, **kwargs)
