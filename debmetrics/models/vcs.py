"""This module defines the Vcs class and vcs table."""

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import Column, Integer, String, DateTime, TIMESTAMP
import ConfigParser
   
config = ConfigParser.RawConfigParser()
config.read('.debmetrics.ini')
DB_URI = config.get('DB', 'DB_URI')

print DB_URI

engine = create_engine(DB_URI)
Base = declarative_base(bind=engine)
Session = scoped_session(sessionmaker(engine))
    
class Vcs(Base):
    __tablename__ = 'vcs'
    __table_args__ =  {'schema': 'metrics'}
                
    ts = Column(TIMESTAMP, primary_key=True)

    svn = Column(Integer)
    darcs = Column(Integer)
    git = Column(Integer)
    bzr = Column(Integer)
    using_vcs = Column(Integer)
    cvs = Column(Integer)
    mtn = Column(Integer)
    total = Column(Integer)
    arch = Column(Integer)
    hg = Column(Integer)
