"""This module creates all the tables from models directory unless the
the database already exists"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from credentials import DATABASE
from models.sources_count import Sources_Count

engine = (create_engine('postgresql://' + DATABASE['dev']['USER']
          + ':' + DATABASE['dev']['PASS'] + '@' + DATABASE['dev']
          ['IP'] + '/debmetrics'))
Base = declarative_base(bind=engine)
Session = scoped_session(sessionmaker(engine))

Base.metadata.create_all(engine)
