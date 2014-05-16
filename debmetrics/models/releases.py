from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import Column, Text, TIMESTAMP, Date
from credentials import DATABASE

"""This module definees the Sources_Count class and sources_count table."""

engine = (create_engine('postgresql://' + DATABASE['dev']['USER']
          + ':' + DATABASE['dev']['PASS'] + '@' + DATABASE['dev']
          ['IP'] + '/debmetrics'))
Base = declarative_base(bind=engine)
Session = scoped_session(sessionmaker(engine))


class Release(Base):
    __tablename__ = 'releases'
    __table_args__ = {'schema': 'metrics'}

    ts = Column(TIMESTAMP, primary_key=True)
    name = Column(Text)
    release_date = Column(Date)
    release_version = Column(Text)

