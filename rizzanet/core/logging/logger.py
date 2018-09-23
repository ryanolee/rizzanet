import logging

def init_logger(app):
    rizzanet_logger = logging.getLogger('rizzanet_logger')
    handle = logging.StreamHandler()
    handle.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    rizzanet_logger.setLevel(logging.DEBUG)
    rizzanet_logger.addHandler(handle)

def get_logger():
    return logging.getLogger('rizzanet_logger')

def format_var(var):
    if isinstance(var, list):
        return ','.join([str(item) for item in var])
    elif isinstance(var, dict):
        return ','.join([str(key)+':'+str(val) for key, val in var.items()])
    return str(var)