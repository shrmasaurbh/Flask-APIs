from marshmallow import Schema, fields, ValidationError, post_load,pre_load,validates,validate
from datetime import datetime
from api.common.constants import *
# from api.common.helpers import validate_email, validate_no

   

class MetaSchema(Schema):
    cc_src_type_id = fields.Integer(required=True)
    cc_project_id = fields.Integer(required=True)
    user_auth_token = fields.String(required=True)
    url = fields.String(required=False)

class DataSchema(Schema):
    object_type = fields.String(required=True)
    login_type = fields.Integer(required=True)
    password = fields.String(required=True,validate=validate.Length(min=6, max=15))
    remember_me = fields.Integer(required=True)

class UserSigninSchema(Schema):
    meta = fields.Nested(MetaSchema)
    data = fields.Nested(DataSchema)

    @pre_load
    def process_data(self, in_data):

        
        for field_key, field_val in in_data.items():
            if field_key == "meta": 

                in_data['meta']['cc_src_type_id'] = int(in_data['meta']['cc_src_type_id'])
                in_data['meta']['cc_project_id'] = int(in_data['meta']['cc_project_id'])
                in_data['meta']['user_auth_token'] = str(in_data['meta']['user_auth_token'])
                in_data['meta']['url'] = str(in_data['meta']['url']).lower().strip()
                
                if not in_data['meta']['user_auth_token']:
                    raise ValidationError("user_auth_token is required")

            
            elif field_key == "data":
                for key,value in in_data['data'].items():
                    if key == 'object_type':
                        if not value:
                            raise ValidationError("object type is not valid")
                        
                        in_data['data'][key] = str(value).lower().strip()

                    elif key == 'password':
                        if in_data['data']['password'] == '':
                            raise ValidationError("password is not valid")



        return in_data 