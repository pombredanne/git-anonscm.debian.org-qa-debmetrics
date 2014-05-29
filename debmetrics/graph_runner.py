#! /usr/bin/python

import os
import subprocess
from config_reader import settings, read_config

read_config('.debmetrics.ini')
directory = settings['DIRECTORY']


def db_fetch(table):
    try:
        conn = psycopg2.connect(conn_str)
    except:
        print "Unable to connect to database."
    cur = conn.cursor()
    table_name = 'metrics.%s' % (table)
    # TODO: Finish db_fetch function


def run():
    for filename in os.listdir(directory):
        name, ext = os.path.splitext(filename)
        if ext == '.py' and not name == '__init__' and 'graph' in name:
            try:
                subprocess.check_output(os.path.join(directory,
                                                     filename))
                print 'success'
            except subprocess.CalledProcessError:
                print 'failure'

if __name__ == '__main__':
    if not os.path.exists('graphs'):
        os.makedirs('graphs')
    run()
