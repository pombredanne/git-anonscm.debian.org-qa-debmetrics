"""This module defines the Releases class and releases table."""

import sqlalchemy
from base import engine, Base, Session
from sqlalchemy import Column, Integer, String, DateTime, TIMESTAMP
    
class Releases(Base):
    __tablename__ = 'releases'
    __table_args__ =  {'schema': 'metrics'}
                
    ts = Column(TIMESTAMP, primary_key=True)

    name = Column(String)
    releasedate = Column(DateTime)
    releaseversion = Column(String)
