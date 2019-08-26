from marshmallow import Schema, fields, ValidationError, post_load,pre_load,validates,validate
from datetime import datetime
from api.common.helper import validate_email, validate_no, validate_url,validate_password
from api.common.constants import *

class MetaSchema(Schema):
    cc_src_type_id = fields.Integer(required=True)
    cc_project_id = fields.Integer(required=True)
    user_auth_token = fields.String(required=True)
    url = fields.String(required=False)

class OtpSchema(Schema):
    otp_value = fields.Integer(required=True)

class PasswordSchema(Schema):
    old_password = fields.String(required=True,validate=validate.Length(min=6, max=15))
    new_password = fields.String(required=True,validate=validate.Length(min=6, max=15))

class DataSchema(Schema):
    object_id = fields.Integer(required=True)
    password = fields.Nested(PasswordSchema)
    otp = fields.Nested(OtpSchema)

class ChangePassSchema(Schema):
    meta = fields.Nested(MetaSchema)
    data = fields.Nested(DataSchema)

    @pre_load
    def process_data(self, in_data):

        # import pdb
        # pdb.set_trace()
        for field_key, field_val in in_data.items():
            if field_key == "meta": 
                in_data['meta']['cc_src_type_id'] = int(in_data['meta']['cc_src_type_id'])
                in_data['meta']['cc_project_id'] = int(in_data['meta']['cc_project_id'])
                in_data['meta']['user_auth_token'] = str(in_data['meta']['user_auth_token'])
                in_data['meta']['url'] = str(in_data['meta']['url']).lower().strip()

                if not validate_url(in_data['meta']['url']):
                    raise ValidationError("project url not valid")
            
            elif field_key == "data":
                for key,value in in_data['data'].items():
                    if key == 'object_id' and not value:
                            raise ValidationError("object id is not valid")
                    elif key == 'password':
                        if not in_data['data'][key]['old_password'] or not in_data['data'][key]['new_password']:
                            raise ValidationError("password is not valid")
                    elif key == 'otp':
                        if not isinstance(value['otp_value'], int) and not len(value['otp_value']) == 6:
                            raise ValidationError("password is not valid")
                      
        return in_data

    @post_load
    def process_data(self, in_data):
        if not validate_password(in_data['data']['password']['old_password']):
            raise ValidationError("Password is not valid")