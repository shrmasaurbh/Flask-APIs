import datetime
import requests
from passlib.hash import pbkdf2_sha256
from api.config.app_config import app_config
from api.common.constants import *
from api.common.settings import *
from itsdangerous import URLSafeSerializer
import logging
import logging.config
__logging_configured = False

CONFIG = app_config()

#parse mongo data
def parse_mongodata(mongodata):
    from bson.objectid import ObjectId
    
    mongodata = mongodata.to_dict()
    for k,v in mongodata.items():
        # print(v)
        if isinstance(v, ObjectId):
           mongodata[k]= str(v)
           if k == "_id":
               mongodata["id"]= mongodata.pop("_id")

        if isinstance(v,datetime.datetime):
           mongodata[k] = (str(v))
    return mongodata

def area_details(pincode=None):

    api_url = 'https://maps.googleapis.com/maps/api/geocode/json?&address=305901&key=AIzaSyBrGrsS5P6YcNjZ2p81QdebhEOdHAz4imY'

    req = requests.get(api_url)
    req = req.json()
    print(req)

def password_hash(user_pass=None):
    resp = {}
    resp['status'] = True
    resp['pass'] = ''

    password_hashed = pbkdf2_sha256.hash(user_pass)

    result = pbkdf2_sha256.verify(user_pass, password_hashed)

    if result:
        resp['pass'] = password_hashed
        return resp

    resp['status'] = False

    return resp    

def password_check(old_pass=None, stored_pass=None):

    return pbkdf2_sha256.verify(old_pass, stored_pass)

def validate_email(email):
    import re
    match = re.match('[^@]+@[^@]+\.[^@]+',email)

    if match == None:
        return False
    else:
        return True

def validate_no(number):
    import re
    
    match = re.match('^[789]\d{9}$',number)

    if match == None:
        return False
    else:
        return True

def validate_url(url):
    import re
        
    match = re.match('^(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$',url)

    if match == None:
        return False
    else:
        return True        

def validate_password(password):
    ''' 
    Consists of 6-15 characters
    Consists of numbers and letters
    At least one big letter and one number
    It should contain #%^&*,./!$?
    The order doesn't matter
    '''
    import re
    
    match = re.match('^(?=.*[#%^&*,.!$?])(?=.*[a-z])(?=.*[A-Z]).{5,15}$')
    
    if match == None:
       return False
    else:
        return True 


def send_sms(to,**sms_details):

    if not to or sms_details == '' or not 'sms_type' in sms_details:
        return False
    sms_type = str(sms_details['sms_type'])
    if sms_details['sms_type'] == '' or not sms_type in SMS_TEMPLATE:
        return False

    # CONFIG = app_config()
    sms_data = SMS_TEMPLATE[sms_type]

    if len(sms_data) != 0:
        if sms_type == "1":
            if 'otp_value' in sms_details and sms_details['otp_value'] != '':
                message = sms_data['message'].replace("#OTPVALUE", str(sms_details['otp_value']))
            else:
                return False

        
        client_details = {}
        default_client = client_name = 'gupshup'
        if 'sms_client' in sms_details and sms_details['sms_client'] != '':
            if sms_details['sms_client'].lower() in SMS_CLIENTS:
                client_name = sms_details['sms_client'].lower()
                client_details = SMS_CLIENTS[sms_details['sms_client'].lower()]
            else:
                client_details = SMS_CLIENTS[default_client]
        else:
                client_details = SMS_CLIENTS[default_client]


        import requests
        if client_name == 'gupshup':
            sms_userid = client_details['sms_userid']
            sms_password = client_details['sms_password']
            sms_url = client_details['sms_url']
            

            data = {"method":"SendMessage","send_to":to,"msg":message,"msg_type":"TEXT",
                    "userid":sms_userid,"auth_scheme":"plain","password":sms_password,
                    "v":1.1,"override_dnd":"true","format": "text"}

            try:
                response = requests.post(sms_url, data = data)
            except Exception as e:
                return False
        
        return True
    else:
        return False    

def generate_otp(length, params):
    resp = {}
    # resp['user'] = 
    resp['create_doc'] = True
    resp['otp_val'] = ''
    if not bool(params):
        return resp
    for key,value in params.items():
        if not value:
            return resp

    from api.models.Mongo_modal import CcUserOtp
    from api.models.configure import mongo_connect
    
    mongo_connect()
    params['cc_is_otp_used'] = False
    import random
    current_time = datetime.datetime.utcnow()

    try:
        payload_list = CcUserOtp.objects(**params).as_pymongo()
        # payload = [item.to_mongo() for item in payload_list ]
        for item in payload_list:
            if item["otp_expiration_time"] > current_time:
                resp['create_doc'] = False
                resp['otp_val'] = item["user_mobile_otp"]
                return resp
    except: pass

    lower = 10**(length-1)
    upper = 10**length - 1
    resp['otp_val'] = random.randint(lower, upper)
    return resp

def verify_otp(params,otp_input):
    resp = {}
    # resp['user'] = 
    resp['message'] = ''
    resp['status'] = False
    if not bool(params):
        resp['message'] = 'pass params'
        # resp['status'] = False
        return resp
    for key,value in params.items():
        if not value:
            resp['message'] = 'pass params values'
            # resp['status'] = False
            return resp

    from api.models.Mongo_modal import CcUserOtp
    from api.models.configure import mongo_connect
    
    mongo_connect()
    
    import random
    current_time = datetime.datetime.utcnow()
    # import pdb
    # pdb.set_trace()
    try:
        params['cc_is_otp_used'] = False
        otp_data = CcUserOtp.objects(**params).as_pymongo() 
        for item in otp_data: 
            if item["otp_expiration_time"] > current_time: 
                if item["user_mobile_otp"] == otp_input:
                    update_otp_data = {}
                    update_otp_data['cc_is_otp_used'] = True
                    update_otp_data['updated_by'] = params['user_auth_id']
                    # update_otp_data['cc_is_otp_used'] = True
                    item.update(**update_otp_data)
                    resp['message'] = 'right otp'
                    resp['status'] = True
                    return resp

                else:
                    resp['message'] = 'otp not match'
                    return resp
            else:
                resp['message'] = 'otp expired'
                return resp
            # else:
        resp['message'] = 'otp not found'
        # resp['status'] = False
        return resp
        # payload = parse_mongodata(payload_list.to_mongo())
    except:
        resp['message'] = 'db error'
        # resp['status'] = False
        return resp


import sendgrid
from sendgrid.helpers.mail import *
def send_email(email_to,**mail_details):

    if email_to == '' or mail_details == '' or not 'email_type' in mail_details:
        return False
    email_type = str(mail_details['email_type'])
    if mail_details['email_type'] == '' or not email_type in EMAIL_TEMPLATE:
        return False

    # CONFIG = app_config()
    email_data = EMAIL_TEMPLATE[email_type]
    content=''

    from_email = 'noreply@carcrew.in'

    with open(email_data['template_path'], 'r') as content_file:
        content = content_file.read()
    # full_mail = email_data['template_path']

    if len(email_data) != 0:
        if email_type == "1":
            if 'otp_value' in mail_details and mail_details['otp_value'] != '':
                message = content.replace("#OTPVALUE", str(mail_details['otp_value']))
            else:
                return False  
        
        # from api.common.settings import *

        client_details = {}
        default_client = client_name = 'sendgrid'
        if 'email_client' in mail_details and mail_details['email_client'] != '':
            if mail_details['email_client'].lower() in email_CLIENTS:
                client_name = mail_details['email_client'].lower()
                client_details = EMAIL_CLIENTS[mail_details['email_client'].lower()]
            else:
                client_details = EMAIL_CLIENTS[default_client]
        else:
                client_details = EMAIL_CLIENTS[default_client]

        import requests
        import json
        if client_name == 'sendgrid' :
            mail_apikey = client_details['mail_apikey']
            sg = sendgrid.SendGridAPIClient(mail_apikey)
            from_email = Email(from_email)
            to_email = Email(email_to)
            content = Content("text/html", msg_html)
            mail = Mail(from_email, subject, to_email, content)

            try:
                response = sg.client.mail.send.post(request_body=mail.get())
            except Exception as e:
                return False

        return True    
    else:
        return False

def send_email_custom(email_to,**mail_details):
    
    from flask import render_template
    from_email = 'noreply@carcrew.in'
    import pdb
    pdb.set_trace()
    msg_html = render_template('forgot.html', **mail_details)
    import os
    from sendgrid import SendGridAPIClient
    from sendgrid.helpers.mail import Mail
    message = Mail(
    from_email=from_email,
    to_emails=email_to,
    subject='Sending with Twilio SendGrid is Fun',
    html_content=msg_html)
    try:
        sg = SendGridAPIClient('nooooo')
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)

    


def get_customer_details(offset= None,**params_dict):
    resp = {}
    resp['is_error'] = 0
    resp['message'] = ''
    resp['data'] = []

    if not bool(params_dict):
        resp['is_error'] = 1
        resp['message'] = 'pass parameters'
        return resp
    for key,value in params_dict.items():
        if not value:
            resp['is_error'] = 1
            resp['message'] = "values can't be empty"
            return resp
        # else:
        #     if key == "user_auth_id"    

    from api.models.Mongo_modal import CcUserProfile
    from api.models.configure import mongo_connect
    
    mongo_connect()

    try:
        payload_list = CcUserProfile.objects(**params_dict)
    except Exception as e:
        resp['is_error'] = 1
        resp['message'] = e
        return resp

    if offset:
        payload_list = payload_list[offset[0]:offset[1]]
    
    payload = [parse_mongodata(item.to_mongo()) for item in payload_list ]
    resp['is_error'] = 0
    resp['message'] = "Found user"
    resp['data'] = payload
    return resp
    # return payload


def get_logger(logger_name=None):
    global __logging_configured
    if not __logging_configured:
        logging.config.dictConfig(CONFIG.LOGGING_CONFIG)
        __logging_configured = True
    logger = logging.getLogger(logger_name or CONFIG.DEFAULT_LOGGER_NAME)
    return logger



def generate_reset_password_url_for_user(user):
    reset_password_url = CONFIG.RESET_PASSWORD_URL.format(code=generate_verification_token(user))
    return reset_password_url

def verify_token(token):
    serializer = URLSafeSerializer(CONFIG.SECRET_KEY)
    try:
        data = serializer.loads(token)
    except Exception as err:
        # TODO Log error here somehow
        return False
    return data

def generate_verification_token(payload):
    serializer = URLSafeSerializer(CONFIG.SECRET_KEY)
    return serializer.dumps(payload)



def get_date_time():
    return datetime.now()


def generate_unique_business_id():
    return str(uuid.uuid4())


def md5_encrypt(val):
    return hashlib.md5(val).hexdigest()


def generateOTP() : 
  
    # Declare a digits variable   
    # which stores all digits
    import math
    import random  
    digits = "0123456789"
    OTP = "" 
  
   # length of password can be chaged 
   # by changing value in range 
    for i in range(4) : 
        OTP += digits[math.floor(random.random() * 10)] 
  
    return OTP
