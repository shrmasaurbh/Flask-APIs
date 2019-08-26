from marshmallow import Schema, fields, ValidationError, post_load,pre_load,validates,validate
from datetime import datetime
from api.common.constants import *

class AccountDetailsSchema(Schema):
	user_account_full_name = fields.String(required=True)
	user_account_mobile_no = fields.String(required=True)
	user_account_email = fields.Email(required=True)
	user_pin_code = fields.Integer(required=True)
	user_geo_code = fields.Dict(required=False)
	user_account_street_address = fields.Dict(required=True)
	user_account_address_landmark = fields.String(required=False)


class UserAccountSchema(Schema):
	user_profile_id = fields.String(null = True, required=False)
	user_auth_id = fields.Integer(required=False)
	# area = fields.Nested(GenericAreaSchema)
	# account_details = fields.Nested(AccountDetailsSchema)
	user_account_default = fields.Boolean(required=False)
	user_account_type = fields.Integer(required=False)
	user_account_full_name = fields.String(required=True)
	user_account_mobile_no = fields.String(required=True,validate=validate.Length(min=10, max=15))
	user_account_email = fields.Email(required=True)
	user_pin_code = fields.Integer(required=True,validate=validate.Length(min=3, max=15))
	user_geo_code = fields.Dict(required=False)
	user_account_street_address = fields.Dict(required=True)
	user_account_address_landmark = fields.String(required=False)

	# @post_load
	# def final_data(self, in_data):
	# 	serialized_data = {}
	# 	fields = ["area","account_details"]
	# 	for field in fields:
	# 		serialized_data.update(in_data[field])
	# 		serialized_data.pop(field)
	# 	return serialized_data

	@post_load
	def final_data(self, in_data):
		# fields = ["account_details"] #area removed
		fields = []
		for field in fields:
			in_data.update(in_data[field])
			in_data.pop(field)
		return in_data
