from marshmallow import Schema, fields, ValidationError, post_load,pre_load,validates,validate
from api.common.helper import validate_url


class MetaSchema(Schema):
    cc_src_type_id = fields.Integer(required=True)
    cc_project_id = fields.Integer(required=True)
    user_auth_token = fields.String(required=True)
    url = fields.String(required=False)

class DataSchema(Schema):
    object_id = fields.Integer(required=True)
    otp_action = fields.Integer(required=True)

class GenerateOtpSchema(Schema):
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

                    elif key == 'otp_action' and not value:
                        raise ValidationError("password is not valid")
                      
        return in_data 