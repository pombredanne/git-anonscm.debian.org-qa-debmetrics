#! /usr/bin/python

import os
import subprocess
import psycopg2
from config_reader import settings, read_config

read_config('.debmetrics.ini')
directory = settings['DIRECTORY']
conn_str = settings['PSYCOPG2_DB_STRING']


def db_fetch(table):
    try:
        conn = psycopg2.connect(conn_str)
    except:
        print "Unable to connect to database."
    cur = conn.cursor()
    table_name = 'metrics.%s' % (table)
    cur.execute('SELECT * FROM ' + table_name + ';')
    res = cur.fetchall()
    # make everything lists of lists containing strings
    for i, row in enumerate(res):
        res[i] = list(row)
        for j, col in enumerate(row):
            res[i][j] = str(col)
    return res


def pack(data):
    return ', '.join(map(str, data))


def run():
    for filename in os.listdir(directory):
        name, ext = os.path.splitext(filename)
        if ext == '.py' and not name == '__init__' and 'graph' in name:
            try:
                data = db_fetch(name.split('_')[0])
                data = pack(data)
                proc = subprocess.Popen([os.path.join(directory, filename)],
                                        stdin=subprocess.PIPE)
                out, err = proc.communicate(data)
                print 'success'
            except subprocess.CalledProcessError:
                print 'failure'

if __name__ == '__main__':
    if not os.path.exists('graphs'):
        os.makedirs('graphs')
    run()
