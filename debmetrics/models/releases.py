"""This module defines the Releases class and releases table."""

import sqlalchemy
from sqlalchemy import engine_from_config
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import Column, Integer, String, DateTime, TIMESTAMP
from credentials import DATABASE
   
engine = engine_from_config(DATABASE, prefix='')
Base = declarative_base(bind=engine)
Session = scoped_session(sessionmaker(engine))
    
class Releases(Base):
    __tablename__ = 'releases'
    __table_args__ =  {'schema': 'metrics'}
                
    ts = Column(TIMESTAMP, primary_key=True)
    name = Column(String)
    sourcefiles = Column(Integer)
    sourcepackages = Column(Integer)
    diskusage = Column(Integer)
    ctags = Column(Integer)
    sloc = Column(Integer)
