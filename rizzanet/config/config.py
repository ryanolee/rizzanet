
import os
from dotenv import DotEnv

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

    ES_CONFIG = [{
        'host': os.getenv('ES_HOST','localhost'),
        'port': os.getenv('ES_PORT', 9200)
    }]

