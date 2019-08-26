# from models.configure import (
#     Model, UNIQUE_ID, CREATED_ON, MODIFIED_ON, DELETED_ON
# )
# from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime,timedelta
from sqlalchemy import Column, String, ForeignKey, Integer, SMALLINT, text,DateTime,Boolean
from api.models.configure import Model


class UserAuthModal(Model):

    __tablename__ = 'cc_user_auth'
    # import pdb
    # pdb.set_trace()
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(4), index=True, unique=True)
    password = Column(String(255))
    temp_password = Column(String(255))
    cc_login_type = Column(Integer, index=True, nullable = True)
    cc_project_id = Column(Integer, index=True, nullable = True)
    cc_user_type_id = Column(String(24), nullable = True)
    object_id = Column(String(24), nullable = True)
    is_active  = Column(Boolean, default=False)
    created_by  = Column(Integer, nullable = True)
    created_at  = Column(DateTime, default=datetime.utcnow)
    updated_by  = Column(Integer, nullable = True)
    updated_at  =  Column(DateTime,default=datetime.utcnow)

    def to_dict(self):
        _d = dict((col, getattr(self, col)) for col in self.__table__.columns.keys())
        return _d
