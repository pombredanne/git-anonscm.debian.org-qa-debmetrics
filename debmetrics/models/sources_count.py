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

class Sources_Count(Base):
    __tablename__ = 'sources_count'

    ts = Column(DateTime, primary_key=True)
    arch = Column(Integer)
    bzr = Column(Integer)
    cvs = Column(Integer)
    darcs = Column(Integer)
    git = Column(Integer)
    hg = Column(Integer)
    mtn = Column(Integer)
    svn = Column(Integer)
    total = Column(Integer)
    using_vcs = Column(Integer)

Base.metadata.create_all()
