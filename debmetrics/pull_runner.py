#! /usr/bin/python

"""This module runs all pull scripts and generates graphs from the data."""

import os
import logging
import datetime
import subprocess
import ConfigParser
import tempfile
os.environ['MPLCONFIGDIR'] = tempfile.mkdtemp()
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import dates
from config_reader import settings, read_config
from runner_helper import db_fetch, db_insert, handle_csv, pack, should_run

try:
    read_config('.debmetrics.ini')
except Exception:
    try:
        read_config('debmetrics/.debmetrics.ini')
    except Exception:
        read_config('../debmetrics/.debmetrics.ini')
directory = settings['PULL_DIRECTORY']
man_dir = settings['MANIFEST_DIRECTORY']
graph_scripts_directory = settings['GRAPH_SCRIPTS_DIRECTORY']
conn_str = settings['PSYCOPG2_DB_STRING']

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def time_series_graph(table, data, cols):
    """Generate a time series graph.

    Keyword args:
    table -- the table the graph is for
    data -- the data to be graphed
    cols -- the column names corresponding to the data
    """
    plt.clf()
    print data
    ts, rest = zip(*data)[0], zip(*data)[1:]
    ts = list(ts)
    for ind, t in enumerate(ts):
        try:
            ts[ind] = datetime.datetime.strptime(t, '%Y-%m-%d %H:%M:%S.%f')
        except Exception:
            ts[ind] = datetime.datetime.strptime(t, '%Y-%m-%d %H:%M:%S')
    fig = plt.figure()
    sub = fig.add_subplot(111)
    fmt = dates.DateFormatter('%Y-%m-%d')
    sub.xaxis.set_major_locator(dates.DayLocator())
    sub.xaxis.set_major_formatter(fmt)
    plt.xticks(rotation=70)
    count = 0
    for ind, r in enumerate(rest):
        if r[0].isdigit():
            count += 1
            sub.plot(ts, r, label=cols[ind+1])
    plt.title("Time series data for " + table)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    if not count == 0:
        plt.savefig(os.path.join('graphs', table + '_timeseries.png'))


def run():
    """The main function that runs the pull scripts and generates graphs."""
    for filename in os.listdir(directory):
        name, ext = os.path.splitext(filename)
        if ext == '.py' and not name == '__init__':
            manifest = ConfigParser.RawConfigParser()
            manifest.read(os.path.join(man_dir, name + '.manifest'))
            print os.path.join(man_dir, name + '.manifest')
            format = manifest.get('script1', 'format')
            if should_run(name+ext, manifest.get('script1', 'freq')):
                try:
                    output = subprocess.check_output(os.path.join(directory,
                                                                  filename))
                    if format == 'csv':
                        header, rows = handle_csv(output)
                    db_insert(header, rows, name)
                except subprocess.CalledProcessError:
                    logger.error('Failure calling process for pull script %s',
                                 filename)
            else:
                logger.error('Did not run pull script %s', filename)

    for filename in os.listdir(graph_scripts_directory):
        name, ext = os.path.splitext(filename)
        if ext == '.py' and not name == '__init__' and 'api' not in name:
            try:
                table = '_'.join(name.split('_')[0:-1])
                data, cols = db_fetch(table)
                config = ConfigParser.RawConfigParser()
                config.read(os.path.join(man_dir, table + '.manifest'))
                graph_type = config.get('script1', 'graph_type')
                if data:
                    if graph_type == 'default':
                        time_series_graph(table, data, cols)
                data = pack(data)
                proc = subprocess.Popen([os.path.join(graph_scripts_directory,
                                        filename)], stdin=subprocess.PIPE)
                out, err = proc.communicate(data)
                if err:
                    logger.error('Failure with graph script for %s: %s',
                                 table, err)
            except subprocess.CalledProcessError:
                logger.error('Failure calling process for graph script for %s',
                             table)

if __name__ == '__main__':
    if not os.path.exists('graphs'):
        os.makedirs('graphs')
    run()
