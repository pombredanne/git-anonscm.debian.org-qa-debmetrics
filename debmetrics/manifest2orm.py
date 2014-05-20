"""This module creates the orm from a manifest file."""

import ConfigParser
import sys
import ntpath

config = ConfigParser.RawConfigParser()


def manifest2orm(manifest):
    """Outputs the orm given a manifest file
    
    Keyword arguments:
    manifest -- location of manifest on file system
    """
    config.read(manifest)
    fieldtypes = config.get('script1', 'fields')
    fieldtypes = ':'.join(fieldtypes.split(', '))
    fieldtypes = fieldtypes.split(':')
    fields = fieldtypes[0::2]
    types = fieldtypes[1::2]

    f = open('models/'+ntpath.basename(file_name).split('.', 1)[0]+'.py', 'w')

    f.write("""\"\"\"This module defines the {0} class and {1} table.\"\"\"

import sqlalchemy
from sqlalchemy import engine_from_config
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import Column, Integer, String, DateTime, TIMESTAMP
from credentials import DATABASE
   
engine = engine_from_config(DATABASE, prefix='')
Base = declarative_base(bind=engine)
Session = scoped_session(sessionmaker(engine))
    
class {0}(Base):
    __tablename__ = '{1}'
    __table_args__ =  {{'schema': 'metrics'}}
                
    ts = Column(TIMESTAMP, primary_key=True)
""".format(table2class(ntpath.basename(file_name).split('.', 1)[0]),
           ntpath.basename(file_name).split('.', 1)[0]))

    for i in range(len(fields)):
        f.write('    '+fields[i]+' = Column('+types[i]+')\n')


def table2class(table):
    """Capitalizes the table name to form a class name"""
    temp = table.split('_')
    for i in range(len(temp)):
        temp[i] = temp[i].capitalize()
    return '_'.join(temp)

if __name__ == '__main__':
    for i in range(1, len(sys.argv)):
        file_name = sys.argv[i]
        manifest2orm(file_name)
