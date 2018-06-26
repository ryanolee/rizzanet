
import os
from dotenv import DotEnv

env_path = os.path.dirname(__file__)+'/../../.env'

if os.path.exists(env_path):
    os.environ.update(DotEnv(env_path).all())

class BaseConfig:
    DEBUG=os.getenv('DEBUG',1)
    SECRET=os.getenv('SECRET',1)

    DB_TYPE = os.getenv('DB_TYPE','sqlite')
    DB_DRIVER = os.getenv('DB_DRIVER','')
    DB_USERNAME = os.getenv('DB_USERNAME','')
    DB_PASSWORD = os.getenv('DB_PASSWORD','')
    DB_HOST = os.getenv('DB_HOST','')
    DB_PORT = os.getenv('DB_PORT','')
    DB_PATH = os.getenv('DB_PATH','')

    ES_CONFIG = [{
        'host': 'localhost',
        'port': 9200
    }]
