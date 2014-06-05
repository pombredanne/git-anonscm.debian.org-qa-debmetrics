#! /usr/bin/python

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

    print """\"\"\"This module defines the {0} class and {1} table.\"\"\"

import sqlalchemy
from base import engine, Base, Session
from sqlalchemy import Column, Integer, String, Date, DateTime, TIMESTAMP
    
class {0}(Base):
    __tablename__ = '{1}'
    __table_args__ =  {{'schema': 'metrics'}}
                
    ts = Column(TIMESTAMP, primary_key=True)
""".format(table2class(ntpath.basename(file_name).split('.', 1)[0]),
           ntpath.basename(file_name).split('.', 1)[0])

    for i in range(len(fields)):
        print'    '+fields[i]+' = Column('+types[i]+')'


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
