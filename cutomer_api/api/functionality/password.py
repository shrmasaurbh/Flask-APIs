from datetime import datetime
# from notifier_async.async_tasks import send_notification
from api.config.app_config import app_config
from api.common.helper import verify_token, md5_encrypt, get_date_time, get_logger
from api.common.helper import generate_reset_password_url_for_user,send_email_custom,password_hash,generateOTP
from api.models.mysql.user_auth import UserAuthModal
from flask import Flask, redirect, url_for
from api.common.response import GeneralResponses
from api.models.configure import mysql_session
from api.models.mongo.account import CcUserOtp
from api.models.configure import mongo_connect
# from api.validation import not_empty, password_according_to_policy
from sqlalchemy import func
import string
from random import *
import datetime
import json

config = app_config()
log = get_logger()


# @not_empty('username', 'RESET-REQ-USERNAME', req=True)
# @valid_username('username', 'SUP-BAD-USERNAME')
def forgot_password(**kwargs):
    data = dict(
        user=dict(
            username=kwargs['username'],
        ),
        otp_for_reset_password=generateOTP(),
        support_phone=config.SUPPORT_PHONE,
        contact_url=config.CONTACT_URL,
    )
    import pdb
    pdb.set_trace()
    mongo_connect()
    mongo_data={}
    mongo_data['user_auth_id'] = kwargs['user_auth_id']
    mongo_data['user_mobile_number'] = kwargs['user_mobile_number']
    mongo_data['user_mobile_otp'] = data['otp_for_reset_password']
    mongo_data['cc_project_id'] = kwargs['cc_project_id']
        # import pdb
        # pdb.set_trace()
    try:
        mongo_obj  = CcUserOtp(**mongo_data).save()
    except Exception as e:
        error = {"error":{"message":e._message, "status_code": 400}}
        return self.response.custom_response("error",error,400) 
    send_email_custom('shrmasaurbh@gmail.in',data =data)
    #send_notification(client='Email', event='ResetPassword', receiver_type='EndUser', data=data)
    
    return dict(
        username=kwargs['username']
    )


# @password_according_to_policy('password', 'RESET-WEAK-PASSWORD')
# @not_empty('token', 'RESET-NULL-VERCODE')



def reset_password(**kwargs):
    token = kwargs['token']
    response = GeneralResponses()
    user_id = verify_token(token)
    if not user_id:
        raise ValueError('RESET-BAD-VERCODE')
    
    user  = mysql_session.query(UserAuthModal).filter(UserAuthModal.username == user_id).first()
    if not user:
        raise ValueError('USER-BAD-ID')
    else:
        characters = string.ascii_letters + string.punctuation  + string.digits
        password =  "".join(choice(characters) for x in range(randint(8, 16)))
        import pdb
        pdb.set_trace()
        user.temp_password = password_hash(password)['pass']
        mysql_session.commit()
        resp={}
        meta = {}
        resp = {'data':password,'meta':meta}
        return response.custom_response("success",resp,201)

def resend_verification(**kwargs):
    user = get_user_by_id(**kwargs)
    if not user.verified:
        data = dict(
            user=dict(
                first_name=user.first_name,
                username=user.username,
            ),
            email_verification_url=generate_email_verification_url_for_user(user),
            resources_url=config.RESOURCES_URL,
            contact_url=config.CONTACT_URL,
        )
        #send_notification(client='Email', event='Verification', receiver_type='EndUser', data=data)
    else:
        raise ValueError('RESEND-VERIFICATION-USER-VERIFIED')
    return dict(username=user.username)


# @password_according_to_policy('new_password', 'RESET-WEAK-PASSWORD')
def change_password(**kwargs):
    user = get_user_by_id(user_id=kwargs['user_id'])
    if not user:
        raise ValueError('USER-BAD-ID')

    if user.password == md5_encrypt(kwargs['old_password']):
        user.password = md5_encrypt(kwargs['new_password'])
        data = dict(
            user=dict(
                first_name=user.first_name,
                username=user.username,
            ),
            login_url=config.LOGIN_URL,
            support_phone=config.SUPPORT_PHONE,
            contact_url=config.CONTACT_URL,
        )
        #send_notification(client='Email', event='ChangePasswordSuccess', receiver_type='EndUser', data=data)
    else:
        raise ValueError('USER-BAD-OLD-PASSWORD')

    return dict(updated="true")


def verify_and_reset_password(**kwargs):
    otp = kwargs['otp']
    new_password = kwargs['new_password']
    response = GeneralResponses()
    mongo_connect()
    # mongo_data['first_name'] = serialized_data['data']['info']['first_name']
    #     mongo_data['last_name'] = serialized_data['data']['info']['last_name']
    #     mongo_data['mobile_no'] = serialized_data['data']['info']['phone_number']
    #     mongo_data['email'] = serialized_data['data']['info']['email_address']
    #     mongo_data['cc_src_type_id'] = serialized_data['meta']['cc_src_type_id']
    #     mongo_data['city_id'] = serialized_data['data']['info']['city_id']
    #     mongo_data['cc_project_id'] = serialized_data['meta']['cc_project_id']
    #     mongo_data['cc_user_type_id'] = serialized_data['meta']['cc_user_type_id']
    #     mongo_data['created_by'] = 1
    #     mongo_data['updated_by'] = 1
    #     mongo_data['user_auth_id'] = user_auth_id
    #     mongo_data['area_id'] = serialized_data['data']['info']['pincode']
    #     # import pdb
    #     # pdb.set_trace()
    #     try:
    #         mongo_obj  = CcUserProfile(**mongo_data).save()
    #     except Exception as e:
    #         mysql_session.delete(sql_obj)
    #         mysql_session.commit()
    #         error = {"error":{"message":e._message, "status_code": 400}}
    #         return self.response.custom_response("error",error,400)  


