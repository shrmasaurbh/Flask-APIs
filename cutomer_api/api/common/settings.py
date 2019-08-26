import os
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'l02bg^70)-uffzvl_rg=+wb+9k6ip&g#%e_v$@+seo445rm538'

SMS_CLIENTS = {
    'gupshup' : {
        'sms_userid' : 0000000,
        'sms_password' : '000000',
        'sms_url' : 'http://enterprise.smsgupshup.com/GatewayAPI/rest'
    }

}

EMAIL_CLIENTS = {
    'sendgrid' : {
        'mail_apikey' : 'nooooooooo',
    }

}


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

# STATIC_URL = '/static/'
# STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

#STATIC_PATH = os.path.join(str(BASE_DIR),'static')
#STATIC_URL = '/static/' # You may find this is already defined as such.
#STATICFILES_DIRS = ( STATIC_PATH, )

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

# AUTH_USER_MODEL = 'login.CCUserAuth'

# GOOGLE_MAPS_API_URL = 'https://maps.googleapis.com/maps/api/geocode/json'
# GOOGLE_MAPS_API_KEY = 'AIzaSyAq67wl7xmFHJMUIkLPULLgPwqWofnNVsk'

# FLASL_LSP_URL = "http://api.flsp.carcrew.in/"
# FLASL_MISC_URL = "http://api.misc.carcrew.in/"
# FLASL_CUSTOMER_URL = "http://api.customer.carcrew.in/"
# PARTS_API = "http://parts.carcrew.in/api"

LSP_COOKIE_FIELDS = [
    "user_auth_id","cc_user_type_id","cc_proect_id",
    "cc_user_cookie_name","cc_user_cookie_type","cc_user_cookie_shared",
    "cc_user_cookie_key","cc_user_cookie_details","cc_user_creation_time",
    "cc_user_cookie_expires_at",
    "cc_user_cookie_storage_engine","cc_user_is_cookie_active",
]

# MEDIA_URL = '/media/'
# MEDIA_ROOT = str(BASE_DIR) + str('/media')

# try:
#     from .local_settings import *
# except:
#     print("No local settings found.")
