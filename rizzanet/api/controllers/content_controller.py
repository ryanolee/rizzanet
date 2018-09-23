from rizzanet.models import Content
from rizzanet.api.validators import required_fields, resource_exists
from rizzanet.api.responses import api_response, api_error
from rizzanet.api.auth import api_auth
from flask import Blueprint

content_controller = Blueprint('content', __name__, url_prefix='/content')


@content_controller.route('/<regex("\d+"):id>',methods=['GET','FETCH'])
@api_auth
@resource_exists(function=Content.get_by_id, name='id')
def get_by_id(id):
    from rizzanet.models import Content
    response = Content.get_by_id(id)
    return handle_get_content_response(response)

@content_controller.route('/path', defaults={'path': ''})
@content_controller.route('/path/<path:path>',methods=['GET','FETCH'])
@api_auth
@resource_exists(function=Content.get_by_path, name='path')
def get_by_path(path):
    from rizzanet.models import Content
    response = Content.get_by_path(path)
    return handle_get_content_response(response)



def handle_get_content_response(response):
    try:
        parts = get_parts()
    except Exception as error:
        return api_error('Error: invalid parts format.',400)
    response_data = response.as_dict()
    if parts != False:
        if any([ part in parts for part in ['all','content_data']]):
            content_data = response.get_content_data()
            response_data['content_data'] = content_data.as_dict()
        if any([ part in parts for part in ['all','content_type']]):
            from rizzanet.models import ContentType
            content_type = response.get_content_type()
            response_data['content_type'] = content_type.as_dict()
    return api_response(response_data)

def get_parts():
    '''gets parts for content objects'''
    from flask import request
    valid_parts = ['content', 'content_data', 'content_type', 'all']
    parts = request.values.get('parts')
    if parts == None:
        return False
    parts = parts.split(',')
    if len(parts) == 0 or not all([part in valid_parts for part in parts]):
        raise Exception('Invalid format for parts')
    else:
        return parts