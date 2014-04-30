import ConfigParser
import sys

config = ConfigParser.RawConfigParser()

def manifest2orm(manifest):
    config.read(manifest)
    tablename = config.get('script1', 'tablename')
    fields = config.get('script1', 'fields')
    types = config.get('script1', 'types')

    print """
    import sqlalchemy
    from sqlalchemy import create_engine
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import sessionmaker, scoped_session
    from sqlalchemy import Column, Integer, String, DateTime
    from credentials import DATABASE

    \"\"\"This module defines the {0} class and {1} table.\"\"\"
    
    engine = (create_engine('postgresql://'+DATABASE['dev']['USER']+':'+DATABASE['dev']
                ['PASS']+'@'+DATABASE['dev']['IP']+'/debmetrics'))
    Base = declarative_base(bind=engine)
    Session = scoped_session(sessionmaker(engine))
    
    class {0}(Base):
        __tablename__ = '{1}'
        __table_args__ =  {{'schema': 'metrics'}}
                
        ts = Column(TIMESTAMP, primary_key=True)
""".format(table2class(tablename), tablename),

    temp = fields.split(', ')
    for i in range(len(temp)):
        print '        '+temp[i]+' = Column('+types.split(', ')[i]+')'

def table2class(table):
    temp = table.split('_')
    for i in range(len(temp)):
        temp[i] = temp[i].capitalize()
    return '_'.join(temp)

if __name__ == '__main__':
    manifest2orm('../examples/manifests/vcs.manifest')

