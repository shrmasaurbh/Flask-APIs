from marshmallow import Schema, fields, ValidationError, post_load,pre_load,validate
from datetime import datetime
from api.common.helper import validate_email, validate_no, validate_url,validate_password
from api.common.constants import *
from bson import ObjectId


class MetaSchema(Schema):
    cc_src_type_id = fields.Integer(required=True)
    cc_user_type_id = fields.Integer(required=True)
    cc_project_id = fields.Integer(required=True)
    project_url = fields.String(required=False)
    social_login = fields.Integer(required=False)

class NotificationSchema(Schema):
    sms = fields.Integer(required=True)
    email = fields.Integer(required=True)

def check_name(self, obj):
    # import pdb
    # pdb.set_trace() 
    if not obj.first_name:
        return 'not valid'
    else:
        return obj['first_name']




class InfoSchema(Schema):
    
    # def load_email(self, value):
    #     return value.upper().strip()
    # import pdb
    # pdb.set_trace() 
    # first_name = fields.Function(lambda obj: obj.first_name.lower().strip() if obj.first_name else False)
    # first_name = fields.Method(check_name)
    first_name = fields.Str(required=True,validate=validate.Length(min=3, max=10))
    username = fields.String(required=True)
    last_name = fields.String(required=True,validate=validate.Length(min=3, max=10))
    email_address = fields.Str(required=True)
    phone_number = fields.String(required=True)
    password = fields.String(required=True,validate=validate.Length(min=6, max=15))
    pincode = fields.String(required=True,validate=validate.Length(min=3, max=8))
    city_id = fields.String(required=True)
    notifications = fields.Nested(NotificationSchema)

    

    # @validates('first_name')
    # def validate_name(self, data):
    #     # import pdb
    #     # pdb.set_trace()
    #     print(data)
    #     if not data['first_name']:
    #         raise ValidationError('Too young!')

class AuthTokenSchema(Schema):
    pass
class DataSchema(Schema):
    info = fields.Nested(InfoSchema)
    auth_token = fields.Nested(AuthTokenSchema) 

class UserAuthSchema(Schema):
    meta = fields.Nested(MetaSchema)
    data = fields.Nested(DataSchema)

    @pre_load
    def process_data(self, in_data):
        # import pdb
        # pdb.set_trace()

        # print(LOGIN_TYPE)
        for field_key, field_val in in_data.items():
            if field_key == "meta": 

                in_data['meta']['cc_src_type_id'] = int(in_data['meta']['cc_src_type_id'])
                in_data['meta']['cc_user_type_id'] = int(in_data['meta']['cc_user_type_id'])
                in_data['meta']['cc_project_id'] = int(in_data['meta']['cc_project_id'])
                in_data['meta']['social_login'] = int(in_data['meta']['social_login'])

                if in_data['meta']['project_url']:
                    in_data['meta']['project_url'] = str(in_data['meta']['project_url']).lower().strip()
                    
                    if not validate_url(in_data['meta']['project_url']):
                        raise ValidationError("project url not valid ")
                else:
                    raise ValidationError("project url is required")
         
            
            elif field_key == "data":
                for key,value in in_data['data']['info'].items():
                    if value == '':
                        raise ValidationError("Fields value can't be empty")
                    elif key == "notifications":
                        in_data['data']['info'][key]['sms'] = int(in_data['data']['info'][key]['sms'])
                        in_data['data']['info'][key]['email'] = int(in_data['data']['info'][key]['email'])
                        if not in_data['data']['info'][key]['sms'] in NOTIFICATION and not in_data['data']['info'][key]['email'] in NOTIFICATION:
                            raise ValidationError("notification field is not valid")

                    else:    
                        in_data['data']['info'][key] = str(value).strip().lower()
                        if key == 'city_id':
                            if len(value) != 24:
                                raise ValidationError("City id is not valid")
                            # else:
                            #     in_data['data']['info'][key] = ObjectId(value)
                        elif key == 'first_name' or key == 'username' or key == 'last_name':
                            in_data['data']['info'][key] = value
                        elif key == 'email_address' and not validate_email(value):   
                            raise ValidationError("Email is not valid")
                        elif key == 'phone_number' and not validate_no(value):    
                            raise ValidationError("phone Number is not valid")
                        elif key == 'password' and not validate_password(value):
                            raise ValidationError("password is not valid")

                      
        return in_data 

    @post_load
    def process_data(self, in_data):
        if in_data['data']['info']['username'] != in_data['data']['info']['email_address'] and validate_no(in_data['data']['info']['phone_number']) is False:
            raise ValidationError("Username is not valid")


