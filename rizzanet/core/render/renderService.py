
from rizzanet.core.logging import get_logger

class RenderService:
    def __init__(self, app):
        self.cfg = app.config['CONTROLLERS']
        self.logger = get_logger()

    def render(self, data, *args, **kwargs):
        print(self.cfg)
        from rizzanet.models import Content
        if isinstance(data, Content):
            return self._find_match(data)
        

    def _render_node(self, node, template_path):
        from rizzanet.events import dispatchEvent
        from rizzanet.core.context import get_render_context
        from flask import render_template
        dispatchEvent('RENDER_NODE', node)
        render_context = get_render_context()
        render_context.push(node)
        res = render_template(template_path,**node.get_template_context())
        render_context.pop()
        return res

    def _find_match(self, node):
        print(self.cfg)
        for controller_name, controller_values in self.cfg['types'].items():
            #preform_checkos on nodes
            if all([ self._check(case, node, value) for case, value in controller_values['match'].items()]):
                self.logger.info('Matched type for node {0!r}'.format(node))
                controller_path = controller_values['template']
                return self._render_node(node, controller_path)
                


    def _check(self, check_name, node, check_value):
        from .matchChecks import CHECKS
        print(check_name)
        if not check_name in CHECKS:
             self.logger.error('Error unknown match case {0} used when trying to match controller type.'.format(check_name))
             return False
        
        #Preform given check on node given mach case
        return CHECKS[check_name](node, check_value)

global render_service
def init_render_service(app):
    global render_service
    render_service = RenderService(app)

def get_render_service():
    global render_service
    return render_service