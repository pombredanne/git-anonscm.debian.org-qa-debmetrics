"""This module defines the Rc_Bug class and rc_bug table."""

import sqlalchemy
from base import engine, Base, Session
from sqlalchemy import Column, Integer, String, Date, DateTime, TIMESTAMP
    
class Rc_Bug(Base):
    __tablename__ = 'rc_bug'
    __table_args__ =  {'schema': 'metrics'}
                

    ts = Column(TIMESTAMP, primary_key=True)
    rc_bugs = Column(Integer)
    with_patch = Column(Integer)
    with_fix = Column(Integer)
    ignored = Column(Integer)
    concern_current_stable = Column(Integer)
    concern_next_release = Column(Integer)
