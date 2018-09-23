from functools import wraps
from .decorators import validator
from rizzanet.api.responses import api_error, http_status

#def required_fields(func,*required_field_data):
#        '''Decorator for required fields'''
#        def arg_wrapper(func):
#            '''partial func so that decorator can be invoked'''
#            from functools import wraps
#            @wraps(func)
#            def required_wrap(*args,**kwargs):
#                from flask import request
#                to_return = []
#                for field in required_field_data:
#                    if request.values.get(field) == None:
#                        to_return.append("'"+field+"'")
#                if to_return != []:  
#                    return api_error('Error required field{0} {1} not set'.format('' if len(to_return)==1 else 's' ,','.join(to_return)),400)
#                return func(*args,**kwargs)
#            return required_wrap
#        return arg_wrapper

@validator
def required_fields(*required_fields):
    from flask import request
    to_return = []
    for field in required_fields:
        if request.values.get(field) == None:
            to_return.append("'"+field+"'")
    if to_return != []:  
        return api_error('Error required field{0} {1} not set'.format('' if len(to_return)==1 else 's' ,','.join(to_return)), http_status.BAD_REQUEST)
    return True

@validator
def resource_exists(function, name, **kwargs):
    if not callable(function) or not name in kwargs:
        return api_error(http_status.INTERNAL_SERVER_ERROR)
    identifier = kwargs[name]
    try:
        data = function(identifier)
        if data != None:
            return True
    except:
        pass
    return api_error('Error: resource not found with identifier {0}'.format(identifier), http_status.NOT_FOUND)


