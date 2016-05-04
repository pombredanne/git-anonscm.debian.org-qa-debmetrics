#! /usr/bin/python3

"""This module creates the orm from a manifest file."""

import configparser
import sys
import os.path
import ntpath
from config_reader import settings, read_config

read_config()
config = configparser.RawConfigParser()


def manifest2orm(manifest):
    """Outputs the orm given a manifest file.
    
    Keyword arguments:
    manifest -- location of manifest on file system
    """
    config.read(manifest)
    fieldtypes = config.get('script1', 'fields')
    fieldtypes = ':'.join(fieldtypes.split(', '))
    fieldtypes = fieldtypes.split(':')
    fields = fieldtypes[0::2]
    types = fieldtypes[1::2]
    override_ts = config.getboolean('script1', 'override_ts')

    print("""\"\"\"This module defines the {0} class and {1} table.\"\"\"

from flask_sqlalchemy import SQLAlchemy
from debmetrics.database import db
    
class {0}(db.Model):
    __tablename__ = '{1}'
""".format(table2class(ntpath.basename(file_name).split('.', 1)[0]),
           ntpath.basename(file_name).split('.', 1)[0]))
    if settings['TEST']:
        print("""    __table_args__ = {'schema': 'metrics_test'}""")
    else:
        print("""    __table_args__ = {'schema': 'metrics'}""")

    if not override_ts:
        print('    ts = db.Column(db.TIMESTAMP, primary_key=True)')
    else:
        print('    an_id = db.Column(db.Integer, primary_key=True,' \
              'autoincrement=True)')
    
    for i in range(len(fields)):
        print('    '+fields[i]+' = db.Column(db.'+types[i]+')')


def table2class(table):
    """Capitalizes the table name to form a class name.
    
    Keyword arguments:
    table -- the table name
    """
    return table.title().replace('_', '')

if __name__ == '__main__':
    for i in range(1, len(sys.argv)):
        file_name = sys.argv[i]
        manifest2orm(file_name)
