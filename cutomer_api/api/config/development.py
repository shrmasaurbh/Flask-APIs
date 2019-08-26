from api.config.base import BaseConfig
from redis import *
class developmentConfig(BaseConfig):
    
    FLASK_APP_NAME = 'Carcrew Development'
    FLASK_DEBUG = True
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    SQLALCHEMY_DATABASE_URI = 'mysql://priyanka:root1234@localhost/cc_customer'
    # MONGO_URI = "mongodb://localhost:27017/customer"
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_POOL_CYCLE = 3600
    SQLALCHEMY_CONVERT_UNICODE = True
    REDIS_HOST = "localhost"
    REDIS_PORT = 6379
    REDIS_PASSWORD = ""
    CACHE_DB = StrictRedis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, decode_responses=True)

    # SALT = "5gz"    