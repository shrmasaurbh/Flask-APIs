__author__ = 'saurabh'

# db = MongoEngine()
from flask_restful import fields, reqparse
from api.models.mongo.account import CcUserProfile
from api.models.configure import mongo_connect
from api.common.helper import parse_mongodata
from api.common.resource_exception import handle_exceptions
# from resources.base_resource import BaseResource as Resource
from mongoengine.queryset.visitor import Q
from flask import Response,request
import json
from api.config.app_config import app_config
import re
from sqlalchemy import text
from flask.views import MethodView
from bson.objectid import ObjectId
from datetime import datetime

CONFIG = app_config()

class UserProfile(MethodView):


    def __init(self):
        self.response = GeneralResponses()
    
    decorators = [handle_exceptions()]
    def get(self,**kwargs):
        mongo_connect()
        data ={}
        id = request.args.get('id')
        user_auth_id = request.args.get('user_auth_id')
        if id:
            user_obj = CcUserProfile.objects.get(id=id)
            if user_obj:
                return Response(json.dumps(parse_mongodata(user_obj)),  mimetype='application/json')
                # resp={}
                # meta = {}
                # resp = {'data':user_obj,'meta':meta}
                # return self.response.custom_response("success",resp,201)

        if user_auth_id:
            user_obj = CcUserProfile.objects.get(user_auth_id=user_auth_id)
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
        auth_id = payload['data']['profiles']['object_id']
        user_obj = CcUserProfile.objects.get(user_auth_id = auth_id)
        if user_obj is None:
            abort(404)
        else:
            profile_data = payload['data']['profiles_details']
            user_obj.update(**profile_data)
    

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
       