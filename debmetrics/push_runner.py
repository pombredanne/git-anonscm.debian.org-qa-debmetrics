#!/usr/bin/python

"""This module handles data from push scripts and generate graphs from the
data."""

import os
import os.path
import logging
import ConfigParser
from config_reader import settings, read_config
from runner_helper import db_fetch, db_insert
from graph_helper import time_series_graph

pkg_dir = os.path.dirname(os.path.abspath(__file__))
read_config(os.path.join(pkg_dir, '.debmetrics.ini'))

directory = settings['PULL_DIRECTORY']
man_dir = settings['MANIFEST_DIRECTORY']
graph_scripts_directory = settings['GRAPH_SCRIPTS_DIRECTORY']
conn_str = settings['PSYCOPG2_DB_STRING']

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def token_matches(man, token):
    """Compares the token to the token in the manifest file.

    Keyword args:
    token -- a push authorization token
    """
    for manifest in os.listdir(man_dir):
        name, ext = os.path.splitext(manifest)
        if name == man:
            config = ConfigParser.RawConfigParser()
            config.read(os.path.join(man_dir, manifest))
            t = config.get('script1', 'token')
            if t == token:
                return True
            else:
                return False


def store(table, header, rows):
    db_insert(header, rows, table)


def graph():
    for filename in os.listdir(man_dir):
        name, ext = os.path.splitext(filename)
        if ext == '.manifest':
            table = name
            data, cols = db_fetch(table)
            config = ConfigParser.RawConfigParser()
            config.read(os.path.join(man_dir, filename))
            t = config.get('script1', 'type')
            if t != 'push':
                return
            graph_type = config.get('script1', 'graph_type')
            if data:
                if graph_type == 'default':
                    time_series_graph(table, data, cols)


if __name__ == '__main__':
    if not os.path.exists('graphs'):
        os.makedirs('graphs')
    graph()