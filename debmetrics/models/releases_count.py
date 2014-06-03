"""This module defines the Releases_Count class and releases_count table."""

import sqlalchemy
from base import engine, Base, Session
from sqlalchemy import Column, Integer, String, DateTime, TIMESTAMP
    
class Releases_Count(Base):
    __tablename__ = 'releases_count'
    __table_args__ =  {'schema': 'metrics'}
                
    ts = Column(TIMESTAMP, primary_key=True)

    name = Column(String)
    sourcefiles = Column(Integer)
    sourcepackages = Column(Integer)
    diskusage = Column(Integer)
    ctags = Column(Integer)
    sloc = Column(Integer)
