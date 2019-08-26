from functools import wraps
from flask_restful import abort
# from errors import AuthorizationFailedError, NotFoundError, AuthorizationTargetError
# from models import session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from api.models.configure import mysql_session
from api.common.response import GeneralResponses
from werkzeug.exceptions import BadRequest
import inspect
# log = get_logger()
# crash_log = get_logger('crash')


def handle_exceptions():
    response = GeneralResponses()
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            try:
                
                return fn(*args, **kwargs)
            except ValueError as val_err:
                # log.error(repr(val_err))
                mysql_session.rollback()
                mysql_session.close()
                
                error = {"error":{"message":val_err, "status_code": 400}}
                return response.custom_response("error",error,400) 
            
            except AttributeError as val_err:
                # log.error(repr(val_err))
                mysql_session.rollback()
                mysql_session.close()
                
                error = {"error":{"message":val_err, "status_code": 400}}
                return response.custom_response("error",error,400) 
            
            except KeyError as key_err:
                # log.error(repr(key_err))
                mysql_session.rollback()
                mysql_session.close()
                
                error = {"error":{"message":key_err, "status_code": 400}}
                return response.custom_response("error",error,400) 
            
            except IOError as io_err:
                # crash_log.exception(io_err)
                mysql_session.rollback()
                mysql_session.close()
                
                error = {"error":{"message":io_err, "status_code": 400}}
                return response.custom_response("error",error,400) 
            # except ValidationError as val_err:
            #     # crash_log.exception(io_err)
            #     mysql_session.rollback()
            #     mysql_session.close()
                
            #     error = {"error":{"message":val_err, "status_code": 400}}
            #     return response.custom_response("error",error,400) 
            
            
            # except AuthorizationFailedError as auth_err:
            #     # log.error(repr(auth_err))
            #     mysql_session.rollback()
            #     mysql_session.close()
                
            #     error = {"error":{"message":auth_err, "status_code": 400}}
            #     return response.custom_response("error",error,400) 
            
            except NoResultFound as nf_err:
                # log.exception(repr(nf_err))
                mysql_session.rollback()
                mysql_session.close()
                
                error = {"error":{"message":nf_err, "status_code": 204}}
                return response.custom_response("error",error,204) 
            
            # except AuthorizationTargetError as auth_target_err:
            #     # log.error(repr(auth_target_err))
            #     mysql_session.rollback()
            #     mysql_session.close()
                
            #     error = {"error":{"message":auth_target_err, "status_code": 400}}
            #     return response.custom_response("error",error,400) 
            
            except IntegrityError as err:
                # crash_log.exception(err)
                mysql_session.rollback()
                mysql_session.close()
                # pattern = "\'[a-z]+(?:_[a-z]*)*\'"
                # matches = re.findall(pattern, err.orig[1])
                
                error = {"error":{"message":err, "status_code": 500}}
                return response.custom_response("error",error,500) 
            
            except SQLAlchemyError as sa_err:
                # crash_log.exception(sa_err)
                mysql_session.rollback()
                mysql_session.close()
                import pdb
                pdb.set_trace()
                error = {"error":{"message":sa_err.orig.args[1], "status_code": 503}}
                return response.custom_response("error",error,503) 
            
            except Exception as exc:
                # crash_log.exception(exc)
                import pdb
                pdb.set_trace()
                mysql_session.rollback()
                mysql_session.close()
                if inspect.isclass(exc) is False:
                    code = 404
                else:
                    code = exc.code

                error = {"error":{"message":None, "status_code": code}}
                return response.custom_response("error",error,code) 

        return decorator

    return wrapper