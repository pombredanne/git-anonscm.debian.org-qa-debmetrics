#! /usr/bin/python

import os
import subprocess
import ConfigParser
import csv
import StringIO
import psycopg2
from config_reader import settings, read_config

read_config('.debmetrics.ini')
directory = settings['DIRECTORY']
conn_str = settings['PSYCOPG2_DB_STRING']


def db_insert(header, rows, table):
    try:
        conn = psycopg2.connect(conn_str)
    except:
        print "Unable to connect to database."
    cur = conn.cursor()
    table_name = 'metrics.%s' % (table)
    for row in rows:
        cur.execute("INSERT INTO " + table_name + " (%s) VALUES (%s);" %
                    (', '.join(header), ','.join(row)))


def handle_csv(data):
    data = csv.reader(StringIO.StringIO(data))
    rows = []
    rownum = 0
    for row in data:
        if rownum == 0:
            header = row
        else:
            rows.append(row)
        rownum += 1
    return header, rows


def run():
    for filename in os.listdir(directory):
        name, ext = os.path.splitext(filename)
        if ext == '.py' and not name == '__init__':
            manifest = ConfigParser.RawConfigParser()
            manifest.read(os.path.join(directory, name + '.manifest'))
            format = manifest.get('script1', 'format')
            try:
                output = subprocess.check_output(os.path.join(directory,
                                                              filename))
                if format == 'csv':
                    header, rows = handle_csv(output)
                db_insert(header, rows, name)
                print 'success'
            except subprocess.CalledProcessError:
                print 'failure'

if __name__ == '__main__':
    run()
