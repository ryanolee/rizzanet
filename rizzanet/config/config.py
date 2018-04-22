
import os
from dotenv import load_dotenv

env_path = os.path.dirname(__file__)+'/../.env'

if os.path.exists(env_path):
    load_dotenv(dotenv_path=env_path)

class BaseConfig:
    DEBUG=os.getenv('DEBUG',1)
    SECRET=os.getenv('SECRET',1)
    DB_TYPE=os.getenv('DB_TYPE','sqlite')
    DB_DRIVER=os.getenv('DB_DRIVER','')
    DB_USERNAME=os.getenv('DB_USERNAME','')
    DB_PASSWORD=os.getenv('DB_PASSWORD','')
    DB_HOST=os.getenv('DB_HOST','')
    DB_PORT=os.getenv('DB_PORT','')
    DB_PATH=os.getenv('DB_PATH','')
