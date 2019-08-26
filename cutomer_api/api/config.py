# from datetime import timedelta
# from os import environ, path
from sys import modules
# import os
# __author__ = 'saurabh'

'''   

        NOT USING



'''
class BaseConfig(object):
    ERROR_404_HELP = False
    PROPAGATE_EXCEPTIONS = True
    # Flask #


class developmentConfig(BaseConfig):
    FLASK_APP_NAME = 'Carcrew Development'
    FLASK_DEBUG = True
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    SQLALCHEMY_DATABASE_URI = 'mysql://saurabh:root@localhost/customer'
    MONGO_URI = "mongodb://localhost:27017/customer"
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_POOL_CYCLE = 3600
    SQLALCHEMY_CONVERT_UNICODE = True
    global_data = {}
    # SALT = "5gz"
    

class productionConfig(BaseConfig):
    FLASK_APP_NAME = 'Carcrew Production'
    FLASK_DEBUG = False
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    SQLALCHEMY_DATABASE_URI = 'mysql://saurabh:root@localhost/customer'
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_POOL_CYCLE = 3600
    SQLALCHEMY_CONVERT_UNICODE = True
    # SALT = "5gz"


config = None


def app_config(cache=True):
    global config
    if cache and config:
        return config
   
    env_name = 'development'
    #env_name = os.getenv('FLASK_ENV')

    print("Environment Running in :"+str(env_name))

    if not env_name:
        raise Exception('Config environment not defined.')

    # module object for this file viz. config.py
    module_object = modules[__name__]
    class_name = '{0}Config'.format(env_name)

    # get class object
    conf = getattr(module_object, class_name)
    conf.config_in_use = class_name
    config = conf
    return conf