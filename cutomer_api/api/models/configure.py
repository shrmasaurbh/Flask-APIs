
from sqlalchemy import (orm, create_engine)
# from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.ext.declarative import declarative_base
from api.config.app_config import app_config


CONFIG = app_config()

Model = declarative_base()

engine = create_engine(CONFIG.SQLALCHEMY_DATABASE_URI )
# Why pool_recycle : http://docs.sqlalchemy.org/en/rel_0_9/dialects/mysql.html#connection-timeouts
_Session = orm.sessionmaker(autocommit=False, autoflush=True, bind=engine)
mysql_session = orm.scoped_session(_Session)
Model.metadata.bind = engine
Model.query = mysql_session.query_property()

def mongo_connect():
    from mongoengine import connect
    DB_NAME = 'customer'
    db = connect(DB_NAME)
    # db = db.customer

# def mongo_con():
#     from pymongo import MongoClient
#     client = MongoClient('mongodb://localhost:27017/')
#     DB_NAME = 'customer'
#     db = client[db]
def mongo_close(mongo_connect):
	db.close()