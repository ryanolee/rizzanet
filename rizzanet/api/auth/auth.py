from rizzanet.api.responses import api_error, http_status

def api_auth(func):
        '''Handles auth for Api'''
        from functools import wraps
        @wraps(func)
        def auth_wrap(*args,**kwargs):
            from flask_login import current_user
            if current_user.is_authenticated and current_user.role > 1000:
                return func(*args,**kwargs)
            from flask import request
            api_key = request.values.get('api_key')
            if api_key == None:
                return api_error('No api key given', http_status.UNAUTHORIZED)
            from rizzanet.models import APIKey
            try:
                key = APIKey.get_by_api_key(api_key)
                authenticated = key.auth(api_key)
            except Exception as error:
                return api_error('Error: authentication failed {0}'.format(error))
            if not authenticated:
                return api_error('Api key invalid', http_status.UNAUTHORIZED)
            return func(*args,**kwargs)
        return auth_wrap