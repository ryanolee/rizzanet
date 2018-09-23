
from rizzanet.models import Content
from rizzanet.core.logging import get_logger
from rizzanet.events import dispatchEvent

class RenderContextStack():
    def __init__(self):
        self._context = []
    
    def push(self, node):
        rz_log = get_logger()
        if not isinstance(node, Content):
            rz_log.warn('Unable to push context for content node {0!s}'.format(node))
            return False
        rz_log.debug('Pushed context {0!r}'.format(node))
        self._context.append(node)
        dispatchEvent('PUSHED_RENDER_CONTEXT', node)

    def current(self):
        if len(self._context) == 0:
            return None
        return self._context[-1]
    
    def get_stack(self):
        return self._context

    def pop(self):
        rz_log = get_logger()
        node = self._context.pop()
        rz_log.debug('Popped context {0!r}'.format(node))
        dispatchEvent('POPPED_RENDER_CONTEXT', node)
        return node



def get_render_context():
    from .requestContextProvider import RequestContextProvider
    return RequestContextProvider(RenderContextStack)

        
