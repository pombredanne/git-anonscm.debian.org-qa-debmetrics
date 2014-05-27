"""This module creates all the tables from models directory unless the
the database already exists"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from models.vcs import Vcs
import ConfigParser

config = ConfigParser.RawConfigParser()
config.read('.debmetrics.ini')
engine = create_engine(config.get('DB', 'DB_URI'))
Base = declarative_base(bind=engine)
Session = scoped_session(sessionmaker(engine))

Base.metadata.create_all(engine)
