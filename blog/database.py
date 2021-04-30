# from peewee import *
#
# user = 'root'
# password = ''
# db_name = 'fastapi'
#
# conn = MySQLDatabase(db_name, password, user=user, host='localhost')
#
#
# class BaseModel(Model):
#     class Meta:
#         database = conn

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = "jdbc:mysql://localhost:3306/fastapi"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
