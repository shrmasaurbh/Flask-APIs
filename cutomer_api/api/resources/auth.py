
# from api.resources.base_import import *
from . import *
from api.models.mysql.user_auth import UserAuthModal
from flask_restful import Resource
from api.common.resource_exception import handle_exceptions
from api.common.constants import *
from api.models.configure import mysql_session
from flask import jsonify
from api.config.app_config import app_config
from api.common.helper import get_logger
from api.serializers.validate_user_signin import UserSigninSchema
from passlib.hash import pbkdf2_sha256
import datetime
from api.models.mongo.account import CcUserProfile
from api.models.configure import mongo_connect
from flask import abort
log = get_logger('apiengine')
# crash_log = get_logger('apiengine')

class UserSignUp(Resource):
    from api.serializers.serialize_user_signup import UserAuthSchema

    serializer = UserAuthSchema()

    def __init__(self):
        self.response = GeneralResponses()

    def post(self,**kwargs):
        
        
        sql_data={}
        error={}
        mongo_data={}
        # import pdb
        # pdb.set_trace()
        sql_data['created_at'] = datetime.datetime.utcnow()
        
        mongo_data['created_at'] = datetime.datetime.utcnow()
        mongo_data['updated_at'] = datetime.datetime.utcnow()
        
        sql_data['is_active'] = True
        mongo_data['is_active'] = True
        # import pdb
        # pdb.set_trace()

        try:
            import json
            payload = request.json

        except BadRequest as e:
            error = {"error":{"message":"Please check meta or data is provided", "status_code": 400 }}
            return self.response.custom_response("error",error,400)
        serialized_data ,serialize_errors = self.serializer.load(payload)
        
        if serialize_errors:
            error = {"error":{"message":serialize_errors, "status_code": 400 }}
            return self.response.custom_response("error",error,400)

        # import pdb
        # pdb.set_trace()
        auth_insert_data ={}
        password_hashed = password_hash(serialized_data['data']['info']['password'])

        if not password_hashed['status']:
            error = {"error":{"message":"password can't be hashed", "status_code": 400 }}
            return self.response.custom_response("error",error,400)

        sql_data['username'] = serialized_data['data']['info']['username']
        sql_data['password'] = password_hashed['pass']
        sql_data['cc_login_type'] = 1
        sql_data['cc_project_id'] = serialized_data['meta']['cc_project_id']
        sql_data['cc_user_type_id'] = serialized_data['meta']['cc_user_type_id']
        sql_data['created_by'] = 1
        sql_data['updated_by'] = 1

        try:
            from api.models.configure import mysql_session

            sql_obj  = UserAuthModal(**sql_data)
            mysql_session.add(sql_obj)
            mysql_session.commit()
            auth_insert_data = sql_obj.to_dict()

        except SQLAlchemyError as exc:
            mysql_session.rollback()
            error = {"error":{"message":exc.orig.args[1], "status_code": 400}}
            return self.response.custom_response("error",error,400)

        if not bool(auth_insert_data):
            mysql_session.rollback()
            error = {"error":{"message":"Mysql Data not insereted in the Database", "status_code": 400}}
            return self.response.custom_response("error",error,400)

        
        
        mongo_connect()
        
        user_auth_id = auth_insert_data['id']

        mongo_data['first_name'] = serialized_data['data']['info']['first_name']
        mongo_data['last_name'] = serialized_data['data']['info']['last_name']
        mongo_data['mobile_no'] = serialized_data['data']['info']['phone_number']
        mongo_data['email'] = serialized_data['data']['info']['email_address']
        mongo_data['cc_src_type_id'] = serialized_data['meta']['cc_src_type_id']
        mongo_data['city_id'] = serialized_data['data']['info']['city_id']
        mongo_data['cc_project_id'] = serialized_data['meta']['cc_project_id']
        mongo_data['cc_user_type_id'] = serialized_data['meta']['cc_user_type_id']
        mongo_data['created_by'] = 1
        mongo_data['updated_by'] = 1
        mongo_data['user_auth_id'] = user_auth_id
        mongo_data['area_id'] = serialized_data['data']['info']['pincode']
        # import pdb
        # pdb.set_trace()
        try:
            mongo_obj  = CcUserProfile(**mongo_data).save()
        except Exception as e:
            mysql_session.delete(sql_obj)
            mysql_session.commit()
            error = {"error":{"message":e._message, "status_code": 400}}
            return self.response.custom_response("error",error,400)  

        mongo_insert_data = parse_mongodata(mongo_obj.to_mongo())

        if not bool(mongo_insert_data):
            error = {"error":{"message":"Mongo Data not insereted in the Database", "status_code": 400}}
            return self.response.custom_response("error",error,400)

        sql_update_data = {}
        sql_update_data['object_id'] = mongo_insert_data['id']
        sql_update_data['updated_at'] = datetime.datetime.utcnow()

        try:
            get_user_obj = mysql_session.query(UserAuthModal).filter(UserAuthModal.id == user_auth_id).update(sql_update_data)
            mysql_session.commit()
            auth_update_data = sql_obj.to_dict()

        except SQLAlchemyError as exc:
            mysql_session.delete(sql_obj)
            mysql_session.commit()
            mongo_obj_delete = CcUserProfile.objects(id=ObjectId(mongo_insert_data['id'])).delete()
            # mysql_session.rollback()
            error = {"error":{"message":exc.orig.args[1], "status_code": 400}}
            return self.response.custom_response("error",error,400)
        
        finally:
            mysql_session.close()

        if not bool(auth_update_data):
            error = {"error":{"message":"Mongo Object Id not insereted in the Database", "status_code": 400}}
            return self.response.custom_response("error",error,400)

        # email_details = {}
        # email_details['email_type'] = '2'
        #email_details['otp_value'] = otp['otp_val']
        # import pdb
        # pdb.set_trace()
        #send_sms = send_sms(customer_details['data'][0]['mobile_no'], **email_details)
        # send_email = send_email(customer_details['data'][0]['email'], **email_details)

        resp={}
        meta = {"cc_project_id":sql_data['cc_project_id'],"cc_user_type_id":sql_data['cc_user_type_id']}
        data = {"city_id":mongo_data['city_id'], "object_id":mongo_insert_data['id'],"verified_status":{"is_email_verified": 0,"is_phone_verified": 0}}
        resp = {'data':data,'meta':meta}
        return self.response.custom_response("success",resp,201)    
        # resp = self.response.common_success(meta, data)
        # return Response(json.dumps(resp), 201,  mimetype='application/json')    

        

class UserAuth(Resource):
    def __init__(self):
        self.response = GeneralResponses()
        from api.models.configure import mysql_session

    decorators = [handle_exceptions()]
    def get(self,**kwargs):

        data=[]

        if kwargs.get('username'):
            username = kwargs.get('username')
            user_obj = mysql_session.query(UserAuthModal).filter(UserAuthModal.username == username).all()
            if not user_obj:
                error = {"error":{"message":"please check username", "status_code": 400}}
                resp = self.response.common_error(error) 
                return Response(json.dumps(resp), 400,  mimetype='application/json')    

            for item in user_obj:
                temp = item.to_dict()
                # temp.pop('created_on')
                data.append(temp)

            return Response(json.dumps(data),  mimetype='application/json')

        elif kwargs.get('user_id'):
            user_id = int(kwargs.get('user_id'))
            user_obj = mysql_session.query(cc_user_auth1).filter(cc_user_auth1.id == user_id).all()
        else:
            user_obj ={}    
        if len(user_obj)==0:
            return Response(json.dumps({'message':'please check user'}),  mimetype='application/json')


class ChangePassword(Resource):
    ''' '''
    # from api.config.app_config import app_config
    # config = app_config()
    
    from api.serializers.serialize_change_password import ChangePassSchema

    serializer = ChangePassSchema()

    def __init__(self):
        self.response = GeneralResponses()

    decorators = [handle_exceptions()]
    def post(self):
        
        # sql_data={}
        error={}
        
        try:
            payload = request.json

        except BadRequest as e:
            error = {"error":{"message":"Please check meta or data is provided", "status_code": 400 }}
            return self.response.custom_response("error",error,400)
        # import pdb
        # pdb.set_trace()
        serialized_data ,serialize_errors = self.serializer.load(payload)

        if serialize_errors:
            error = {"error":{"message":serialize_errors, "status_code": 400 }}
            return self.response.custom_response("error",error,400)

        user_id = str(serialized_data['data']['object_id'])
        new_hashed_pass = password_hash(serialized_data['data']['password']['new_password'])

        cc_project_id = serialized_data['meta']['cc_project_id']
        cc_src_type_id = serialized_data['meta']['cc_src_type_id']
        user_auth_token = serialized_data['meta']['user_auth_token']

        from api.models.configure import mysql_session

        # import pdb
        # pdb.set_trace()
        sql_obj  = mysql_session.query(UserAuthModal).filter(UserAuthModal.id == user_id).first()
        if sql_obj is None:
            mysql_session.rollback()
            error = {"error":{"message":"User not found", "status_code": 400}}
            return self.response.custom_response("error",error,400)
        
        auth_data = sql_obj.to_dict()
        # import pdb 
        # pdb.set_trace() 
        match_old_pass = password_check(serialized_data['data']['password']['old_password'],auth_data['password'])
        if not match_old_pass:
            error = {"error":{"message":"password not match", "status_code": 400}}
            return self.response.custom_response("error",error,400) 

        otp_data={
            "user_auth_id" : user_id,
            "cc_project_id" : cc_project_id
        }

        otp_flag = verify_otp(otp_data, serialized_data['data']['otp']['otp_value'])

        if otp_flag['status']:

            sql_update_data = {}
            sql_update_data['password'] = new_hashed_pass['pass']
            sql_update_data['updated_at'] = datetime.datetime.utcnow()
            sql_update_data['updated_by'] = 1

            sql_obj = mysql_session.query(UserAuthModal).filter(UserAuthModal.id == user_id).update(sql_update_data)
            mysql_session.commit()
            # auth_update_data = sql_obj.to_dict()

            if not sql_obj:
                error = {"error":{"message":"User password not updated", "status_code": 400}}
                return self.response.custom_response("error",error,400)

            resp ={}
            meta = {"cc_project_id":cc_project_id, "cc_src_type_id":cc_src_type_id}
            data = {"object_id":user_id,"user_auth_token":user_auth_token,"response":"Password Changed"}
            resp = {'data':data,'meta':meta}
            
            return self.response.custom_response("success",resp,201)
        else:      
            error = {"error":{"message":otp_flag['message'], "status_code": 400}}
            return self.response.custom_response("error",error,400) 


class GenerateOtp(Resource):
    
    from api.serializers.serialize_generate_otp import GenerateOtpSchema

    serializer = GenerateOtpSchema()

    def __init__(self):
        self.response = GeneralResponses()

    # decorators = [handle_exceptions()]
    def post(self):
        
        error={}
        
        try:
            payload = request.json

        except BadRequest as e:
            error = {"error":{"message":"Please check meta or data is provided", "status_code": 400 }}
            return self.response.custom_response("error",error,400)
        
        serialized_data ,serialize_errors = self.serializer.load(payload)

        if serialize_errors:
            error = {"error":{"message":serialize_errors, "status_code": 400 }}
            return self.response.custom_response("error",error,400)

        from api.common.helper import get_customer_details,send_sms,generate_otp,send_email

        user_query = {}
        user_query['user_auth_id'] = serialized_data['data']['object_id']
        
        offset = None
        customer_details = get_customer_details(offset,**user_query)

        if customer_details['is_error']:
            error = {"error":{"message":customer_details['message'], "status_code": 400 }}
            return self.response.custom_response("error",error,400)
        
        otp_data = {
            "user_auth_id" : serialized_data['data']['object_id'],
            "cc_project_id" : serialized_data['meta']['cc_project_id'],
            "otp_generated_for" : serialized_data['data']['otp_action']
        }

        otp = generate_otp(6, otp_data)

        if not otp['otp_val']:
            error = {"error":{"message":"can't generate otp", "status_code": 400}}
            return self.response.custom_response("error",error,400)

        if otp['create_doc']:
            otp_creation_time = datetime.datetime.utcnow()

            otp_expiration_time = otp_creation_time + datetime.timedelta(minutes = 10)

            from api.models.Mongo_modal import CcUserOtp
            from api.models.configure import mongo_connect
            
            mongo_connect()

            user_data = {}

            user_data['user_auth_id'] = serialized_data['data']['object_id']
            user_data['user_profile_id'] = str(customer_details['data'][0]['id'])
            user_data['user_mobile_number'] = customer_details['data'][0]['mobile_no']
            user_data['user_mobile_otp'] = otp['otp_val']
            user_data['otp_generated_for'] = serialized_data['data']['otp_action']
            user_data['cc_project_id'] = serialized_data['meta']['cc_project_id']
            user_data['cc_is_otp_used'] = False
            user_data['cc_user_type_id'] = customer_details['data'][0]['cc_user_type_id']
            user_data['otp_creation_time'] = otp_creation_time
            user_data['otp_expiration_time'] = otp_expiration_time
            user_data['is_active'] = True
            user_data['created_by'] = str(customer_details['data'][0]['id'])
            user_data['created_at'] = datetime.datetime.utcnow()
            user_data['updated_by'] = str(customer_details['data'][0]['id'])
            
            try:
                mongo_obj  = CcUserOtp(**user_data).save()
            except Exception as e:
                error = {"error":{"message":e, "status_code": 400}}
                return self.response.custom_response("error",error,400)  

            mongo_insert_data = parse_mongodata(mongo_obj.to_mongo())

        # if not bool(mongo_insert_data):
        #     error = {"error":{"message":"Mongo Data not insereted in the Database", "status_code": 400}}
        #     return self.response.custom_response("error",error,400)

        # sms_type = email_type = '1'
        sms_email_details={}
        sms_email_details['email_type'] = sms_email_details['sms_type'] = '1'
        sms_email_details['otp_value'] = otp['otp_val']
        # import pdb
        # pdb.set_trace()
        send_sms = send_sms(customer_details['data'][0]['mobile_no'], **sms_email_details)
        # send_email = send_email(customer_details['data'][0]['email'], **sms_email_details)

        if not send_email and not send_sms:
            # CcUserOtp(id=ObjectId(mongo_insert_data['id'])).delete()
            error = {"error":{"message":"sms and email not send", "status_code": 400 }}
            return self.response.custom_response("error",error,400)

        cc_project_id = serialized_data['meta']['cc_project_id']
        cc_src_type_id = serialized_data['meta']['cc_src_type_id']
        user_auth_token = serialized_data['meta']['user_auth_token']

        resp = {}
        meta = {"cc_project_id":cc_project_id, "cc_src_type_id":cc_src_type_id}
        data = {
                    "object_id":serialized_data['data']['object_id'],
                    "user_auth_token":user_auth_token,
                    "response":"OTP sent",
                    "otp_action":1
                }
        resp = {'data':data,'meta':meta}
        
        return self.response.custom_response("success",resp,201)    

class UserSignIn(Resource):
    

    

    def __init__(self):
        self.user_schema = UserSigninSchema()
        self.userauth_schema = UserSigninSchema(only=('password','temp_password'))
        self.response = GeneralResponses()
        CONFIG = app_config()
        self.cache_db = CONFIG.CACHE_DB


    decorators = [handle_exceptions()]
    def post(self):
       
        # abort(500)
        log.debug('Params : %s', request.json)
        sql_data={}
        error={}
        serialized_data ,serialize_errors = self.user_schema.load(request.json)
        if serialize_errors:
            error = {"error":{"message":serialize_errors, "status_code": 400 }}
            return self.response.custom_response("error",error,400)

        login_object = serialized_data['data']['object_type']
        login_type = serialized_data['data']['login_type']
        if login_type == "0":
            login_object_valid = validate_email(login_object)

            if not login_object_valid:
                error = {"error":{"message":"lemail is not proper", "status_code": 400 }}
                resp = self.response.common_error(error) 
                return Response(json.dumps(resp), 400,  mimetype='application/json')                
        
        elif login_type == "1":
            login_object_valid = validate_no(login_object)
            
            if not login_object_valid:
                error = {"error":{"message":"lemail is not proper", "status_code": 400 }}
                resp = self.response.common_error(error) 
                return Response(json.dumps(resp), 400,  mimetype='application/json')

        # else:
        #     error = {"error":{"message":"login type is not proper", "status_code": 400 }}
        #     return self.response.custom_response("error",error,400)
        
        cc_project_id = serialized_data['meta']['cc_project_id']
        cc_src_type_id = serialized_data['meta']['cc_src_type_id']
        user_auth_token = serialized_data['meta']['user_auth_token']

        sql_obj  = mysql_session.query(UserAuthModal).filter(UserAuthModal.username == login_object).first()

        if sql_obj is None:
            error = {"error":{"message":"User not found", "status_code": 400}}
            return self.response.custom_response("error",error,400)
        auth_data = self.userauth_schema.dump(sql_obj)
        if pbkdf2_sha256.verify(serialized_data['data']['password'], auth_data.data['temp_password']):
             error = {"error":{"message":"please change your temporary password ", "status_code": 400}}
             return self.response.custom_response("error",error,400)

             # to be redirected to change password page if user has given temporary password
             # more code to be written




        if not pbkdf2_sha256.verify(serialized_data['data']['password'], auth_data.data['password']):
             error = {"error":{"message":"password not match", "status_code": 400}}
             return self.response.custom_response("error",error,400)

        meta= {
               "src_type_id": 1,
               "cc_project_id": 2,
               "city_id": 3,
               "status": 200,
               "is_error": 0,
               "messages": []
            }
        data = [{
                   "object_id": "1234",
                   "cookie": [{
                       "is_cookie_set": 1,
                       "remember_me": 1,
                       "is_global": 0
                   }],
                   "auth_token": [{
                       "auth_id": "xuwesssdd"
                   }],
                   "response": "Successful"
                }]
        return jsonify({
                'meta': meta,
                'data': data,
            })