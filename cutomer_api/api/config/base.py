import os
from datetime import datetime
class BaseConfig(object):
    global_data = {}
	
    ERROR_404_HELP = False
    PROPAGATE_EXCEPTIONS = True
    BASE_URL = ''
    # Logging #
    SECRET_KEY = 'avengersendgame'
    SUPPORT_PHONE = '9783694447'
    CONTACT_URL = 'www.carcrew.com'
    API_URL = 'http://127.0.0.1:5000' # to be changed for frontend url
    EMAIL_VERIFICATION_URL = '%s/verify/{code}' % API_URL
    RESET_PASSWORD_URL = '%s/password/reset/{code}' % API_URL
    DEFAULT_LOGGER_NAME = datetime.now().strftime('apiengine_%d-%m-%Y.log')
    LOGGING_CONFIG = dict(
    version=1,
    formatters={
        'compact': {'format': '%(asctime)s [%(levelname)-8s] %(name)-10s : %(message)s'},
        'err_report': {'format': '%(asctime)s\n%(message)s'}
    },
    handlers={
        'apiengine': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'formatter': 'compact',
            'level': 'DEBUG',
            'filename': os.path.join(os.getcwd(), 'logs/api/'+DEFAULT_LOGGER_NAME),
            'interval': 1,
            'when': 'midnight',
            'encoding': 'utf8'
        },
        'critical_err': {
            'class': 'logging.handlers.SMTPHandler',
            'formatter': 'err_report',
            'mailhost': ("localhost", 25),
            'fromaddr': 'shrmasaurbh@gmail.com',
            'toaddrs': [
                'shrmasaurbh@gmail.com',
                'saurabh.sharma1@carcrew.in'
            ],
            'subject': 'Customer-ApiEngine-Production : Something bad happened'
        },
        'default': {
            'class': 'logging.StreamHandler',
            'formatter': 'compact'
        }
    },
    loggers={
        'default': {
            'handlers': ['default'],
            'level': 'DEBUG'
        },
        'apiengine': {
            'handlers': ['apiengine'],
            'level': 'DEBUG',
            'propagate': False
        },
        'crash': {
            'handlers': ['critical_err', 'apiengine'],
            'level': 'ERROR',
            'propagate': False
        }
    }
)

    # Flask #
