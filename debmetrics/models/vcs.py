"""This module defines the Vcs class and vcs table."""

import sqlalchemy
from base import engine, Base, Session
from sqlalchemy import Column, Integer, String, DateTime, TIMESTAMP
    
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
