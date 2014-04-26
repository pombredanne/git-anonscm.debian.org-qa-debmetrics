import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import Column, Integer, String, DateTime
from credentials import DATABASE

engine = create_engine('postgresql://'+DATABASE['dev']['USER']+':'+DATABASE['dev']['PASS']+'@'+DATABASE['dev']['IP']+'/debmetrics') 
Base = declarative_base(bind=engine)
Session = scoped_session(sessionmaker(engine))

class Sources_Count(Base):
    __tablename__ = 'sources_count'

    ts = Column(DateTime, primary_key=True)
    vcs_arch = Column(Integer)
    vcs_bzr = Column(Integer)
    vcs_cvs = Column(Integer)
    vcs_darcs = Column(Integer)
    vcs_git = Column(Integer)
    vcs_hg = Column(Integer)
    vcs_mtn = Column(Integer)
    vcs_svn = Column(Integer)
    format_3native = Column(Integer)
    format_3quilt = Column(Integer)

Base.metadata.create_all()
