from flask_cors import CORS
from flask_restful import Api

from api.resources.auth import UserSignUp, UserAuth,ChangePassword, UserSignIn, GenerateOtp
from api.resources.profile import UserProfile
from api.resources.reset_password import Forgot,Change,Reset,ResetNewpassword,VerifyOtp
from api.resources.account import UserAccount


def create_restful_api(app):
    api = Api(app)
    CORS(app, resources={r"*": {"origins": "*"}})

    api.add_resource(UserSignUp, '/api/signup' ,endpoint="signup user")
    api.add_resource(UserSignIn, '/api/signin' ,endpoint="signin user")
    api.add_resource(GenerateOtp, '/api/generateotp' ,endpoint="generate otp")
    # api.add_resource(ChangePassword, '/api/changepassword' ,endpoint="change user password ")
    api.add_resource(UserAccount, '/api/account' ,endpoint="account operations ")
    api.add_resource(UserProfile, '/api/profile' ,endpoint="save,delete and put operations on profile")
    api.add_resource(UserProfile, '/api/profile/<string:id>' ,endpoint="get profile")
    api.add_resource(Forgot, '/password/reset')
    api.add_resource(VerifyOtp, '/verify-otp')
    # api.add_resource(Change, '/password/change')
    # api.add_resource(Reset, '/password/reset/<string:token>', endpoint='reset_password')
    api.add_resource(ResetNewpassword, '/reset-form', endpoint='reset via password')
    # api.add_resource(UserAuth, '/user_auth/<string:username>' ,endpoint="get user username")
    # api.add_resource(UserAuth, '/user_auth/<int:user_id>' ,endpoint="get user id ")
    # api.add_resource(UserAuth, '/user_auth' ,endpoint="get all")
    # api.add_resource(UserProfile, '/user_profile/<string:username>' ,endpoint="get all data")
    # api.add_resource(Bookings, '/bookings/<string:booking_id>',endpoint="delete booking")


#have to add every url in this also for checking if end-point is present or not
def end_points():
    api_routes= [
        '/api/signup',
        '/api/signin',
        '/api/changepassword',
        '/api/generateotp'
    ]

    return api_routes