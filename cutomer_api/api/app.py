from flask import Flask, request
from api.config.app_config import app_config
from api.routes import create_restful_api
from api.middleware.auth import SimpleMiddleWare
from werkzeug.exceptions import default_exceptions
config = app_config()

def create_app(**kwargs):

    app = Flask(config.FLASK_APP_NAME,template_folder='templates')
    #get all the config
    app.config.from_object(config)
    # config.BASE_URL = app.root_path
    #implementing middleware
    app.wsgi_app = SimpleMiddleWare(app.wsgi_app)
    # import pdb
    # pdb.set_trace()
    # for code, ex in default_exceptions.items():
    #     app.errorhandler(code)(_handle_http_exception)
    
    if kwargs.get('rest'):
        create_restful_api(app)
    else:
    	print("CAN'T START THE APP")
    # TODO This should be somewhere else but here
    return app

# def on_404(e):
#   print('on_404')
#   return jsonify(dict(error='Not found')), 404
