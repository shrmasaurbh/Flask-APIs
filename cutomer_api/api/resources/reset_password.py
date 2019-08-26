__author__ = 'saurabh'
from api.functionality.password import reset_password, forgot_password, change_password
from api.common.helper import get_logger,parse_mongodata
# from onehop.models import session
from flask import Response,request
from flask_restful import Resource
from api.models.mysql.user_auth import UserAuthModal
from api.models.configure import mysql_session
from api.common.resource_exception import handle_exceptions


log = get_logger('apiengine')


class Forgot(Resource):

    decorators = [handle_exceptions()]
    def post(self):
        """
        @api {post} /password/reset Forgot password
        @apiName ForgotPassword
        @apiGroup User

        @apiParam {String} username User name

        @apiSuccess {String} username User name

        @apiSuccessExample e.g. Success-Response
        HTTP/1.1 200 OK
        {
            "username": "test@onehop.com"
        }
        @apiErrorExample Database error
        HTTP/1.1 400 Bad Request
        {"message": "API-ERR-DB"}

        @apiErrorExample Username required
        HTTP/1.1 400 Bad Request
        {"message": "RESET-REQ-USERNAME"}

        @apiErrorExample Requested Username Not available
        HTTP/1.1 400 Bad Request
        {"message": "RESET-NOTFOUND-USERNAME"}

        """
        source=None
        payload = request.json
        username = payload['username']
        user_obj = mysql_session.query(UserAuthModal).filter(UserAuthModal.username == username).all()
        if not user_obj:
            error = {"error":{"message":"please check username", "status_code": 400}}
            resp = self.response.common_error(error) 
            return Response(json.dumps(resp), 400,  mimetype='application/json')    

        log.info('Params : %s', request.json)
        response = forgot_password(**payload)
        # session.commit()
        return response
class ResetNewpassword(Resource):

    def post(self):
        """
        @api {post} /password/reset Forgot password
        @apiName ForgotPassword
        @apiGroup User

        @apiParam {String} username User name

        @apiSuccess {String} username User name

        @apiSuccessExample e.g. Success-Response
        HTTP/1.1 200 OK
        {
            "username": "test@onehop.com"
        }
        @apiErrorExample Database error
        HTTP/1.1 400 Bad Request
        {"message": "API-ERR-DB"}

        @apiErrorExample Username required
        HTTP/1.1 400 Bad Request
        {"message": "RESET-REQ-USERNAME"}

        @apiErrorExample Requested Username Not available
        HTTP/1.1 400 Bad Request
        {"message": "RESET-NOTFOUND-USERNAME"}

        """
        source=None
        payload = request.json
        username = payload['username']
        user_obj = mysql_session.query(UserAuthModal).filter(UserAuthModal.username == username).all()
        if not user_obj:
            error = {"error":{"message":"please check username", "status_code": 400}}
            resp = self.response.common_error(error) 
            return Response(json.dumps(resp), 400,  mimetype='application/json')    

        log.info('Params : %s', request.json)
        response = forgot_password(username)
        # session.commit()
        return response







class Reset(Resource):

    decorators = [handle_exceptions()]
    def get(self, token):
        """
        @api {post} /password/reset/{token} Reset password
        @apiName ResetPassword
        @apiGroup User

        @apiParam {string} password new password

        @apiSuccess {String} username User name

        @apiSuccessExample e.g. Success-Response
        HTTP/1.1 200 OK
        {
            "username": "test@onehop.com"
        }

        @apiErrorExample Requested Username Not available
        HTTP/1.1 400 Bad Request
        {"message": "RESET-NOTFOUND-USERNAME"}

         @apiErrorExample Token is wrong
        HTTP/1.1 400 Bad request
        {"message": "RESET-BAD-VERCODE"}

        @apiErrorExample Token is blank
        HTTP/1.1 400 Bad request
        {"message": "RESET-NULL-VERCODE"}

        @apiErrorExample Weak password
        HTTP/1.1 400 Bad request
        {"message": "RESET-WEAK-PASSWORD"}

        """
        params = {}
        params.update(dict(token=token))
        response = reset_password(**params)
        # session.commit()
        return response


class Change(Resource):


    decorators = [handle_exceptions()]
    def post(self):
        """
        @api {post} /password/change change password
        @apiName ChangePassword
        @apiGroup User

        @apiParam {string} new_password new password
        @apiParam {string} old_password old password
        @apiSuccess {String} username User name
        @apiHeader {String} Authorization
        @apiSuccessExample e.g. Success-Response
        HTTP/1.1 200 OK
        {
            "updated": "true"
        }

        @apiErrorExample Old password is blank
        HTTP/1.1 400 Bad Request
        {"message": "CHANGE-REQ-OLD-PASSWORD"}

        @apiErrorExample New Password is blank
        HTTP/1.1 400 Bad request
        {"message": "CHANGE-REQ-NEW-PASSWORD"}

        @apiErrorExample Weak password
        HTTP/1.1 400 Bad request
        {"message": "RESET-WEAK-PASSWORD"}

        @apiErrorExample Old Password does not match
        HTTP/1.1 400 Bad request
        {"message": "USER-BAD-PASSWORD"}

        """

        params = change_password_request_format.parse_args()
        params['user_id'] = current_identity.id
        response = change_password(**params)
        # session.commit()
        return response


class VerifyOtp(Resource):


    decorators = [handle_exceptions()]
    def post(self):
        
        payload = request.json
        response = verify_and_reset_password(**params)
        # session.commit()
        return response


