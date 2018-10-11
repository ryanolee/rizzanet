from yaml import safe_load, YAMLError
from rizzanet.core.logging import get_logger
import os

def load_yaml_config(file):
    data = {}
    rz_log = get_logger()
    
    if not os.path.exists(file):
        rz_log.warn('Config file {0} not loaded. File does not exist.'.format(file))
        return data
    
    with open(file, 'rt') as file_stream:
        try:
            data = safe_load(file_stream)
            return data
        except YAMLError as error:
            rz_log.error('Failed to load config {0}. Reason {1}'.format(file, error.message))
    
    return data
    
