
from functools import wraps

def validator(validator_func):
    '''Decorator fro validator functions'''
    @wraps(validator_func)
    def param_validator_decorator(*validator_args, **validator_kwargs):
        '''Function that takes args during paramitisation of validator function'''
        def validator_decorator(function):
            '''the actual wrapper for the function the validator is attached to'''
            @wraps(validator_decorator)
            def real_wrapper(*args, **kwargs):
                '''intrunal wrapper for validator so args can be passed to real function'''
                # Passes decorator given args then real passed args to func 
                v_res = validator_func(*[*validator_args,*args], **{**validator_kwargs, **kwargs})
                '''if validator res is not valid pass forwards validation error'''
                if v_res != True:
                    return v_res
                return function(*args, **kwargs)
            #Reassign function name to wrapper
            real_wrapper.__name__ = function.__name__
            return real_wrapper
        return validator_decorator
    return param_validator_decorator

