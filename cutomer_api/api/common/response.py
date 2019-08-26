# from flask import request
from flask import Response
import json
# from api.config.app_config import app_config
from api.common.constants import MIMETYPE
from api.common.constants import response_codes
# CONFIG = app_config()

class GeneralResponses():
    def __init__(self):
        self.status = 200
        self.is_error = 0
        self.messages = []
        self.mimetype = MIMETYPE['json']

    def custom_response(self, resp_type=None,resp=None,code=None,extra=None):
        if resp_type is None and resp is None and code is None:
            return print("Please pass proper data in proper format")


        code = str(code)
        if "error" == str(resp_type):
            if not 'error' in resp: 
                return print("Please check error key is not passed")
            
            return self.common_error(code, resp)
        
        if not 'meta' in resp or not 'data' in resp:
            return print("Please check meta and data keys are passed")

        return self._common_success(code, resp, extra)    

    def common_error(self,code,resp):
        error_message = resp['error']['message'] if resp['error']['message'] else response_codes[code]
        error_status = code
        resp = {}
        data = []
        meta = {"is_error":1, "status":error_status, "message":error_message}
        final_resp = {"meta":meta, "data": data}
        return Response(json.dumps(final_resp), status=error_status, mimetype=self.mimetype)
        # return jsonify({"result":{ "is_error":1, "status":"failure", "status_code":error_status,
             # "message":error_message }}),400
    
    def _common_success(self, code, resp, extra):
        data = []
        meta ={"is_error":self.is_error, "status":self.status, "message":self.messages}
        meta.update(resp['meta'])
        data.append(resp['data'])

        final_resp = {"meta":meta, "data": data}
        return Response(json.dumps(final_resp), status=code, mimetype=self.mimetype)

    # def common_success(self,rec_meta=None, rec_data=None):
    #     # message = data['message']
    #     resp = {}
    #     data = []
    #     meta ={"is_error":self.is_error, "status":self.status, "message":self.messages}
    #     meta.update(rec_meta)
    #     data.append(rec_data)

    #     resp = {"meta":meta, "data": data}
    #     return resp