from flask import request
from api.config.app_config import app_config
from api.routes import end_points
from flask import Response,request
import json


class SimpleMiddleWare(object):
    allowed_methods = frozenset([
        'GET',
        'HEAD',
        'POST',
        'DELETE',
        'PUT',
        'PATCH',
        'OPTIONS'
    ])
    bodyless_methods = frozenset(['GET', 'HEAD', 'OPTIONS', 'DELETE'])

    def __init__(self, app):
        self.app = app 

    def __call__(self, environ, start_response):

        # method = environ.get('HTTP_X_HTTP_METHOD_OVERRIDE', '').upper()
        # if method in self.allowed_methods:
        #     method = method.encode('ascii', 'replace')
        #     environ['REQUEST_METHOD'] = method
        # if method in self.bodyless_methods:
        #     environ['CONTENT_LENGTH'] = '0'

        
        CONFIG = app_config()
        _data = {"extra_header":"checker"}
        CONFIG.global_data.update(_data)

        #check if end-point is present or not
        # import pdb
        # pdb.set_trace()
        end_point = end_points()
        # import pdb
        # pdb.set_trace()
        if not environ['REQUEST_URI'] in end_point:
            # from flask import Response
            from api.common.response import GeneralResponses
            response = GeneralResponses()
            error = {"message":"api end point in not valid", "status_code": 400}
            # return Response(json.dumps(error), status=200)
            # return "saurabh"
            # return response.custom_response("error",error,400) 

        # recieved_data = json.loads(request.header)
        '''{'wsgi.version': (1, 0), 'wsgi.url_scheme': 'http', 'wsgi.input': <_io.BufferedReader name=5>, 'wsgi.errors': <_io.TextIOWrapper name='<stderr>' mode='w' encoding='UTF-8'>, 'wsgi.multithread': True, 'wsgi.multiprocess': False, 'wsgi.run_once': False, 'werkzeug.server.shutdown': <function WSGIRequestHandler.make_environ.<locals>.shutdown_server at 0x7fdf659cf9d8>, 'SERVER_SOFTWARE': 'Werkzeug/0.15.1', 'REQUEST_METHOD': 'POST', 'SCRIPT_NAME': '', 'PATH_INFO': '/changepassword', 'QUERY_STRING': '', 'REQUEST_URI': '/changepassword', 'RAW_URI': '/changepassword', 'REMOTE_ADDR': '127.0.0.1', 'REMOTE_PORT': 49894, 'SERVER_NAME': '127.0.0.1', 'SERVER_PORT': '5000', 'SERVER_PROTOCOL': 'HTTP/1.1', 'CONTENT_TYPE': 'multipart/form-data; boundary=--------------------------925404267749196881638502', 'HTTP_CACHE_CONTROL': 'no-cache', 'HTTP_POSTMAN_TOKEN': '84e09a84-2648-4461-b47e-79e2800214b1', 'HTTP_USER_AGENT': 'PostmanRuntime/7.6.0', 'HTTP_ACCEPT': '*/*', 'HTTP_HOST': '127.0.0.1:5000', 'HTTP_ACCEPT_ENCODING': 'gzip, deflate', 'CONTENT_LENGTH': '498', 'HTTP_CONNECTION': 'keep-alive', 'werkzeug.request': <BaseRequest 'http://127.0.0.1:5000/changepassword' [POST]>}'''
        print(environ)
        # print(request)

        # CONFIG['extra_header'] = "check" 
        # How do I access request object here.
        print("I'm in middleware")
        # request.headers['Access-Token'] = 
        return self.app(environ, start_response)


        # def __call__(self, environ, resp):
        # errorlog = environ['wsgi.errors']
        # pprint.pprint(('REQUEST', environ), stream=errorlog)

        # def log_response(status, headers, *args):
        #     pprint.pprint(('RESPONSE', status, headers), stream=errorlog)
        #     return resp(status, headers, *args)

        # return self._app(environ, log_response)