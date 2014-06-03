#! /usr/bin/python

import os
import datetime
import subprocess
import psycopg2
import matplotlib.pyplot as plt
from matplotlib import dates
from config_reader import settings, read_config

import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

read_config('.debmetrics.ini')
directory = settings['GRAPH_SCRIPTS_DIRECTORY']
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
    cols = [desc[0] for desc in cur.description]
    # make everything lists of lists containing strings
    for i, row in enumerate(res):
        res[i] = list(row)
        for j, col in enumerate(row):
            res[i][j] = str(col)
    return res, cols


def pack(data):
    return ', '.join(map(str, data))


def time_series_graph(table, data, cols):
    ts, rest = zip(*data)[0], zip(*data)[1:]
    ts = list(ts)
    for ind, t in enumerate(ts):
        ts[ind] = datetime.datetime.strptime(t, '%Y-%m-%d %H:%M:%S.%f')
    fig = plt.figure()
    sub = fig.add_subplot(111)
    fmt = dates.DateFormatter('%Y-%m-%d')
    sub.xaxis.set_major_locator(dates.DayLocator())
    sub.xaxis.set_major_formatter(fmt)
    plt.xticks(rotation=70)
    for ind, r in enumerate(rest):
        sub.plot(ts, r, label=cols[ind+1])
    plt.title("Time series data for " + table)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig('graphs/' + table + '_timeseries.png')


def run():
    for filename in os.listdir(directory):
        name, ext = os.path.splitext(filename)
        if ext == '.py' and not name == '__init__' and 'api' not in name:
            try:
                table = name.split('_')[0]
                data, cols = db_fetch(table)
                time_series_graph(table, data, cols)
                data = pack(data)
                proc = subprocess.Popen([os.path.join(directory, filename)],
                                        stdin=subprocess.PIPE)
                out, err = proc.communicate(data)
                if not err:
                    print 'success'
                else:
                    print 'failure'
            except subprocess.CalledProcessError:
                print 'failure'

if __name__ == '__main__':
    if not os.path.exists('graphs'):
        os.makedirs('graphs')
    run()
