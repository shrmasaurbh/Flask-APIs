from api.common.response import GeneralResponses
from flask import Response,request
from api.config.app_config import app_config
from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError
from api.common.helper import generate_otp, verify_otp,send_sms,parse_mongodata, password_hash,password_check, validate_email, validate_no
from bson.objectid import ObjectId
from werkzeug.exceptions import BadRequest