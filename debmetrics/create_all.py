"""This module creates all the tables from models directory unless the
the database already exists"""

from sqlalchemy import engine_from_config
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from config_reader import settings, read_config
from models.vcs import Vcs

read_config('.debmetrics.ini')
engine = engine_from_config(settings, prefix='')
Base = declarative_base(bind=engine)
Session = scoped_session(sessionmaker(engine))

Base.metadata.create_all(engine)
