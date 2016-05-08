#!/usr/bin/python3

"""This module handles data from push scripts and generate graphs from the
data."""

import os
import os.path
import logging
import configparser
from debmetrics.config_reader import settings, read_config
from debmetrics.runner_helper import db_fetch, db_insert
from debmetrics.graph_helper import time_series_graph

pkg_dir = os.path.dirname(os.path.abspath(__file__))
read_config()

directory = settings['PULL_DIRECTORY']
man_dir = settings['MANIFEST_DIRECTORY']
graph_scripts_directory = settings['GRAPH_SCRIPTS_DIRECTORY']
graph_dir = settings['GRAPH_DIRECTORY']

if not os.path.isabs(directory):
    directory = os.path.join(pkg_dir, directory)
if not os.path.isabs(man_dir):
    man_dir = os.path.join(pkg_dir, man_dir)
if not os.path.isabs(graph_scripts_directory):
    graph_scripts_directory = os.path.join(pkg_dir, graph_scripts_directory)

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
            config = configparser.RawConfigParser()
            config.read(os.path.join(man_dir, manifest))
            t = config.get('script1', 'token')
            if t == token:
                return True
            else:
                return False


def store(table, header, rows):
    try:
        db_insert(header, rows, table)
        return True
    except:
        return False


def graph():
    for filename in os.listdir(man_dir):
        name, ext = os.path.splitext(filename)
        if ext == '.manifest':
            table = name
            data, cols = db_fetch(table)
            config = configparser.RawConfigParser()
            config.read(os.path.join(man_dir, filename))
            t = config.get('script1', 'type')
            if t != 'push':
                return
            graph_type = config.get('script1', 'graph_type')
            if data:
                if graph_type == 'default':
                    time_series_graph(table, data, cols)


if __name__ == '__main__':
    if not os.path.exists(graph_dir):
        os.makedirs(graph_dir)
    graph()
