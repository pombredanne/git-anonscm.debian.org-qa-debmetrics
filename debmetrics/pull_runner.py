#! /usr/bin/python

"""This module runs all pull scripts and generates graphs from the data."""

import os
import logging
import subprocess
import ConfigParser
from graph_helper import time_series_graph
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


def run():
    """The main function that runs the pull scripts and generates graphs."""
    for filename in os.listdir(directory):
        name, ext = os.path.splitext(filename)
        if ext == '.py' and not name == '__init__':
            manifest = ConfigParser.RawConfigParser()
            manifest.read(os.path.join(man_dir, name + '.manifest'))
            t = manifest.get('script1', 'type')
            if t == 'pull':
                print os.path.join(man_dir, name + '.manifest')
                format = manifest.get('script1', 'format')
                if should_run(name+ext, manifest.get('script1', 'freq')):
                    try:
                        output = subprocess.check_output(os.path.join(
                            directory, filename))
                        if format == 'csv':
                            header, rows = handle_csv(output)
                        db_insert(header, rows, name)
                    except subprocess.CalledProcessError:
                        msg = 'Failure calling process for pull script %s'
                        logger.error(msg, filename)
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
                t = config.get('script1', 'type')
                graph_type = config.get('script1', 'graph_type')
                if t == 'pull':
                    if data:
                        if graph_type == 'default':
                            time_series_graph(table, data, cols)
                    data = pack(data)
                    proc = subprocess.Popen([os.path.join(
                                            graph_scripts_directory,
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
