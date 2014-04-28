import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import Column, Integer, String, DateTime
from credentials import DATABASE

"""This module definees the Sources_Count class and sources_count table."""

engine = (create_engine('postgresql://'+DATABASE['dev']['USER']+':'+DATABASE['dev']
        ['PASS']+'@'+DATABASE['dev']['IP']+'/debmetrics'))
Base = declarative_base(bind=engine)
Session = scoped_session(sessionmaker(engine))

class Releases_Count(Base):
    __tablename__ = 'releases_count'
    __table_args__ =  {'schema': 'metrics'}

    ts = Column(TIMESTAMP, primary_key=True)
    name = Column(Text)
    source_files = Column(Integer)
    source_packages = Column(Integer)
    disk_usage = Column(Integer)
    ctags = Column(Integer)
    sloc = Column(Integer)
    
