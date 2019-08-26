from api.config.development import developmentConfig
from api.config.production import productionConfig
from sys import modules
import os


config = None
def app_config(cache=True):
    global config
    if cache and config:
        return config
   
    env_name = os.getenv('FLASK_ENV') if os.getenv('FLASK_ENV') else 'development' 
    # print(app.root_path)
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