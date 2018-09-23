from flask import request, has_request_context, Response
from rizzanet.core.logging import get_logger
from rizzanet.models import Content
class VarnishTagger:
    
    TAG_PREFIX = 'RZ_PURGE_'
    HEADER_NAME = 'X-rizzanet-ban-tags'

    def __init__(self):
        self._tags = []

    def tag_node(self, node):
        rz_log = get_logger()
        if not has_request_context():
            rz_log.warn('Tried to tag node {0!r} outside of an app context'.format(node))
            return False
        
        if isinstance(node, Content):
            rz_log.warn('Cannot tag a none node object')
        
        self.add_tag(self.get_tag_for_node(node))
        self.add_tag(self.get_tag_for_content_data(node.content_data))
    
    def get_tag_for_node(self, node):
        return self.TAG_PREFIX + 'CONTENT_NODE_{0!s}'.format(node.get_id())

    def get_tag_for_content_data(self, content_data):
        return self.TAG_PREFIX + 'CONTENT_DATA_{0!s}'.format(content_data.get_id())

    def add_tag(self, value):
        if value in self._tags:
            return False
        self._tags.append(value)
        return True
    
    def has_tags(self):
        return len(self._tags) != 0
    
    def get_header_string(self):
        return ','.join(self._tags)

    def add_headers_to_response(self, response):
        if not isinstance(response, Response):
            rz_log = get_logger()
            rz_log.warn('Tried to add headers to a non response object during varnish tagging.')
            return response
        response.headers[self.HEADER_NAME] = self.get_header_string()
        return response


def get_varnish_tagger():
    from rizzanet.core.context import RequestContextProvider
    return RequestContextProvider(VarnishTagger)