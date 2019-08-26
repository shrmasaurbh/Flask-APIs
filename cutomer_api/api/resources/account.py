from api.common.helper import parse_mongodata
from . import *
from api.models.mysql.user_auth import UserAuthModal
from api.models.mongo.account import CcUserAccount
from api.models.mongo.account import CcUserProfile
from flask_restful import Resource
from api.common.resource_exception import handle_exceptions
from api.common.constants import *
from api.models.configure import mongo_connect
from api.models.configure import mysql_session
from flask import jsonify
from api.common.resource_exception import handle_exceptions
from api.config.app_config import app_config
from api.common.helper import get_logger,parse_mongodata
from api.serializers.user_account_schema import UserAccountSchema
from passlib.hash import pbkdf2_sha256
import datetime
import json
from flask import abort
log = get_logger('apiengine')


class UserAccount(Resource):

    def __init__(self,*args,**kwargs):
        self.user_schema = UserAccountSchema()
        self.userauth_schema = UserAccountSchema(only=('password',))
        self.response = GeneralResponses()
        CONFIG = app_config()
        self.cache_db = CONFIG.CACHE_DB


    def get(self,obj_id=None,user_id=None):

        mongo_connect()
        data ={}
        id = request.args.get('id')
        user_auth_id = request.args.get('user_auth_id')
        if id is None and user_auth_id is None:
            user_obj = CcUserAccount.objects.get.all()
            if user_obj:
                return Response(json.dumps(parse_mongodata(user_obj)),  mimetype='application/json')
            else:
                abort(404)

        if id:
            user_obj = CcUserAccount.objects.get(id=id)
            if user_obj:
                return Response(json.dumps(parse_mongodata(user_obj)),  mimetype='application/json')
                # resp={}
                # meta = {}
                # resp = {'data':user_obj,'meta':meta}
                # return self.response.custom_response("success",resp,201)

        if user_auth_id:
            user_obj = CcUserAccount.objects.get(user_auth_id=user_auth_id)
            if user_obj:
                return Response(json.dumps(parse_mongodata(user_obj)),  mimetype='application/json')
        
        abort(404)














    decorators = [handle_exceptions()]
    def put(self,**kwargs):
       
        mongo_connect()
        payload = request.json
        import pdb
        pdb.set_trace()
        profile_data={}
        auth_id = payload['data']['accounts']['object_id']
        profile_id = payload['data']['accounts']['object_account_id']
        account_obj = CcUserAccount.objects.get(user_auth_id = auth_id)
        profile_obj = CcUserProfile.objects.get(id = profile_id)
        if account_obj is None or profile_obj is None :
            abort(404)
        else:
            profile_data['user_account_full_name'] = payload['data']['account_details']['first_name'] + " " + payload['data']['account_details']['last_name']
            profile_data['city_id'] = payload['data']['account_details']['city_id']
            profile_data['user_account_street_address'] = payload['data']['account_details']['addresses']
            profile_data['state_id'] = payload['data']['account_details']['state_id']
            profile_data['user_pin_code'] = payload['data']['account_details']['pin_code']
            profile_data['user_account_mobile_no'] = payload['data']['account_details']['mobile_no']
            account_obj.update(**profile_data)
        resp={}
        meta = {"cc_project_id":payload['meta']['cc_project_id'],"src_type_id":payload['meta']['src_type_id']
                ,"city_id":payload['data']['account_details']['city_id'],}
        data = {"Object_id":payload['data']['accounts']['object_id'], "Object_account_id":payload['data']['accounts']['object_account_id'],"City_id":payload['data']['account_details']['city_id'],"user_auth_token": 0}
        resp = {'data':data,'meta':meta}
        return self.response.custom_response("success",resp,201)    



    decorators = [handle_exceptions()]
    def post(self,**kwargs):
        mongo_connect()
        payload = request.json
        import pdb
        pdb.set_trace()
        account_data={}
        account_data.update({'user_auth_id':payload['data']['accounts']['object_id']})
        account_data.update({'cc_user_type_id':payload['data']['accounts']['object_account_id']})
        account_data.update({'user_account_email':"ankush.rai@gmail.com"})
        account_data.update({'user_account_type':1})
        account_data.update({'user_pin_code':4110050})
        account_data.update({'created_by':123})
        account_data.update({'updated_by':13})
        account_data.update({'cc_project_id':payload['meta']['cc_project_id']})
        account_data.update({'user_account_full_name':payload['data']['account_details']['first_name'] +" "+payload['data']['account_details']['last_name']})
        account_data.update({'city_id':payload['data']['account_details']['city_id']})
        account_data.update({'user_account_street_address':payload['data']['account_details']['addresses']})
        account_data.update({'user_account_address_landmark':payload['data']['account_details']['landmark']})
        account_data.update({'state_id':payload['data']['account_details']['state_id']})
        account_data.update({'user_account_mobile_no':payload['data']['account_details']['mobile_no']})
        account = CcUserAccount(**account_data)
        account.save()

        resp={}
        meta = {"cc_project_id":payload['meta']['cc_project_id'],"src_type_id":payload['meta']['src_type_id']
                ,"city_id":payload['data']['account_details']['city_id'],}
        data = {"Object_id":payload['data']['accounts']['object_id'], "Object_account_id":payload['data']['accounts']['object_account_id'],"City_id":payload['data']['account_details']['city_id'],"user_auth_token": 0}
        resp = {'data':data,'meta':meta}
        return self.response.custom_response("success",resp,201) 

    decorators = [handle_exceptions()]
    def delete(self,**kwargs):
        mongo_connect()
        payload = request.json
        profile_data={}
        profile_id = payload['data']['profiles']['object_id']
        user_obj = CcUserProfile.objects.get(id = profile_id).to_mongo()
        if user_obj is None:
            abort(404)
        else:
            #profile_data = payload['data']['profiles_details']
            user_obj['is_active'] = False
            user_obj.update(**user_obj)