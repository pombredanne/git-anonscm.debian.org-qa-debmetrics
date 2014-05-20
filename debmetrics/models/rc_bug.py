
    """This module defines the Rc_Bug class and rc_bug table."""

    import sqlalchemy
    from sqlalchemy import create_engine
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import sessionmaker, scoped_session
    from sqlalchemy import Column, Integer, String, DateTime, TIMESTAMP
    from credentials import DATABASE
   
    engine = (create_engine('postgresql://'+DATABASE['dev']['USER']+':'+DATABASE['dev']
              ['PASS']+'@'+DATABASE['dev']['IP']+'/debmetrics'))
    Base = declarative_base(bind=engine)
    Session = scoped_session(sessionmaker(engine))
    
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
