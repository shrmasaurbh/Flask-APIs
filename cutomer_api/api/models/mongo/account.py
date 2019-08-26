from mongoengine import Document, EmbeddedDocument, fields
from flask import Flask
from datetime import datetime,timedelta
from pytz import timezone
india = timezone('Asia/Kolkata')  # to be made generic for different country
class CcUserOtp(Document):
	
	user_auth_id = fields.IntField(required=True)
	user_profile_id = fields.ObjectIdField(null = True, required=False)
	user_account_id = fields.ObjectIdField(null = True,required=False)
	user_mobile_number = fields.StringField(required=True)
	user_mobile_otp = fields.IntField(required=True)
	# otp_generated_for = fields.IntField(required=False)  # need to be changed
	cc_project_id = fields.IntField(required=True)
	cc_is_otp_used = fields.BooleanField(required=False)
	cc_user_type_id = fields.IntField(required=False)
	otp_creation_time = fields.DateTimeField(default=datetime.now(india))
	otp_expiration_time = fields.DateTimeField(default=datetime.now(india)+timedelta(seconds = 60))
	is_active = fields.BooleanField(default=False, required=False)
	created_by = fields.ObjectIdField(required=False)
	created_at = fields.DateTimeField()
	updated_by = fields.ObjectIdField(required=False)
	updated_at = fields.DateTimeField(default=datetime.utcnow)

	def save(self, *args, **kwargs):
		# if not self.created_at:
		# 	self.created_at = datetime.utcnow()
		# if not self.otp_creation_time: 9923891761
		# 	self.otp_creation_time = datetime.utcnow()

		return super(CcUserOtp, self).save(*args, **kwargs)


class CcUserProfile(Document):

	user_auth_id = fields.IntField(required=False)
	first_name = fields.StringField(required=False)
	last_name = fields.StringField(required=False)
	mobile_no = fields.StringField(required=False)
	email = fields.EmailField(required=False)
	gender = fields.IntField(required=False)
	alternate_number = fields.StringField(required=False)
	is_profile_verified = fields.DynamicField(required=False)
	cc_src_type_id = fields.IntField(null = True, required=False)
	cc_project_id = fields.IntField(required=False)
	cc_default_profile = fields.BooleanField(required=False)
	profile_type = fields.IntField(required=False)
	profile_others_info = fields.DynamicField(required=False)
	profile_max_lock_limit = fields.IntField(required=False)
	is_profile_active = fields.BooleanField(required=False)
	country_id = fields.StringField(null = True, required=False)
	state_id = fields.StringField(null = True, required=False)
	city_id = fields.StringField(null = True, required=False)
	area_id = fields.IntField(null = True, required=False)
	cc_user_type_id = fields.IntField(null = True, required=False)
	is_active = fields.BooleanField(default=False, required=False)
	created_by = fields.IntField(required=False)
	created_at = fields.DateTimeField(required=False)
	updated_by = fields.IntField(required=False)
	updated_at = fields.DateTimeField(default=datetime.utcnow)



	def save(self, *args, **kwargs):
		# if not self.created_at:
		# 	self.created_at = datetime.utcnow()

		return super(CcUserProfile, self).save(*args, **kwargs)

class CcUserAccount(Document):

	ACCOUNT_TYPE =  (
		(0,"HOME"),
		(1,"OFFICE"),
		(2,"OTHERS"),
		)

	user_auth_id = fields.IntField(required=True)
	user_profile_id = fields.ObjectIdField(null=True, required=False) #
	cc_project_id = fields.ObjectIdField(required=True) #
	cc_user_type_id = fields.ObjectIdField(null=True, required=False) #
	user_account_full_name = fields.StringField(required=True)
	user_account_mobile_no = fields.StringField(required=True)
	user_account_email = fields.EmailField(required=True)
	user_account_street_address = fields.DynamicField(required=True)
	user_account_address_landmark = fields.StringField(required=False)
	user_account_default = fields.BooleanField(required=False)
	user_account_type = fields.IntField(required=True)
	country_id = fields.ObjectIdField(null = True, required=False)
	state_id = fields.ObjectIdField(null = True, required=False)
	city_id = fields.ObjectIdField(null = True, required=False)
	area_id = fields.ObjectIdField(null = True, required=False)
	user_pin_code = fields.IntField(required=True)
	# user_geo_code = fields.GeoPointField(required=True)
	user_geo_code = fields.DynamicField(required=False)
	is_active = fields.BooleanField(default=False, required=False)
	created_by = fields.IntField(required=True)
	created_at = fields.DateTimeField()
	updated_by = fields.IntField(required=True)
	updated_at = fields.DateTimeField(default=datetime.utcnow)



	def save(self, *args, **kwargs):
		import pdb
		pdb.set_trace()
		if not self.created_at:
			self.created_at = datetime.utcnow()

		return super(CcUserAccount, self).save(*args, **kwargs)

class CcUserCookies(Document):
	user_auth_id = fields.IntField(required=True,unique=True)
	cc_src_type_id = fields.ObjectIdField(null = True, required=False)
	cc_project_id = fields.ObjectIdField(required=True)
	cc_user_type_id = fields.ObjectIdField(null = True, required=False)
	cc_user_cookie_name = fields.StringField(required=True)
	cc_user_cookie_type = fields.IntField(required=True)
	cc_user_cookie_shared = fields.IntField(required=True)
	cc_user_cookie_key = fields.IntField(required=True)
	cc_user_cookie_details = fields.DynamicField(required=True)
	cc_user_cookie_creation_time = fields.DateTimeField()
	cc_user_cookie_expires_at = fields.DateTimeField()
	cc_user_is_cookie_active = fields.BooleanField(default=False, required=False)
	cc_user_cookie_storage_engine = fields.IntField(required=True)
	is_active = fields.BooleanField(default=False, required=False)
	created_by = fields.IntField(required=True)
	created_at = fields.DateTimeField()
	updated_by = fields.IntField(required=True)
	updated_at = fields.DateTimeField(default=datetime.utcnow)

	def save(self, *args, **kwargs):
		if not self.created_at:
			self.created_at = datetime.utcnow()

		return super(CcUserCookies, self).save(*args, **kwargs)


class CcUserVehicleInfo(Document):
	user_auth_id = fields.IntField(required=True,unique=True)
	user_vehicle_id = fields.ObjectIdField(required=False)#needs to be true
	user_profile_id = fields.ObjectIdField(required=False)#needs to be true
	user_account_id = fields.ObjectIdField(required=False)#needs to be true
	cc_project_id = fields.ObjectIdField(required=True)
	cc_user_type_id = fields.ObjectIdField(required=False)# needs to be true
	user_vehicle_vin_number = fields.IntField(required=True)
	user_vehicle_registration_number = fields.IntField(required=True)
	user_vehicle_registration_date = fields.DateTimeField()
	user_vehicle_others_info = fields.DynamicField(required=False)
	user_vehicle_odometer_history = fields.DynamicField(required=True)
	is_active = fields.BooleanField(default=False, required=False)
	created_by = fields.IntField(required=True)
	created_at = fields.DateTimeField()
	updated_by = fields.IntField(required=True)
	updated_at = fields.DateTimeField(default=datetime.utcnow)

	def save(self, *args, **kwargs):
		if not self.created_at:
			self.created_at = datetime.utcnow()

		return super(CcUserVehicleInfo, self).save(*args, **kwargs)

