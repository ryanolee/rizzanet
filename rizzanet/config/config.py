
import os
from dotenv import DotEnv
from yaml import safe_load
from rizzanet.config.loader import load_yaml_config
env_path = os.path.dirname(__file__)+'/../../.env'

if os.path.exists(env_path):
    os.environ.update(DotEnv(env_path).all())



class BaseConfig:
    DEBUG=os.getenv('DEBUG',1)
    SECRET=os.getenv('SECRET',1)
    DB_TYPE = os.getenv('DB_TYPE','sqllite')
    DB_DRIVER = os.getenv('DB_DRIVER','')
    DB_USERNAME = os.getenv('DB_USERNAME','')
    DB_PASSWORD = os.getenv('DB_PASSWORD','')
    DB_HOST = os.getenv('DB_HOST','')
    DB_PORT = os.getenv('DB_PORT','3306')
    DB_NAME = os.getenv('DB_NAME','')

    RIZZANET_ENV = os.getenv('RIZZANET_ENV', 'prod')

    VARNISH_CONFIG = {
        'VARNISH_PURGE_SERVER_HOSTS': os.getenv('VARNISH_PURGE_SERVER_HOSTS', ''),
        'VARNISH_ENABLED': os.getenv('VARNISH_ENABLED', False)
    }

    ES_CONFIG = [{
        'host': os.getenv('ES_HOST','localhost'),
        'port': os.getenv('ES_PORT', 9200)
    }]

    API_VERSION = 'v1'

    IMAGES = {
        'PATH': '/images',
        'ALLOWED_FORMATS': ['webp','png','gif','jpg'],
        'FORCE_CONVERT': False,
        'AUTO_DUMP_IMAGES': True,
        'DEFAULT_ALIAS': 'normal',
        'DEFAULT_FORMAT': 'png',
        'ALIASES': {
            'normal': [{
                
            }],
            'icon': [{
                'filter': 'resize',
                'args': {
                    'size':(800,800)
                }
            },{
                'filter': 'rotate',
                'args':{
                    'angle': 90
                }
            }]
        }
    }
    
    CONTROLLERS =  load_yaml_config(os.path.dirname(__file__)+'/controllers.yml')

