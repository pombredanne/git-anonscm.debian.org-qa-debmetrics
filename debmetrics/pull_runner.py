#! /usr/bin/python3

"""This module runs all pull scripts and generates graphs from the data."""

import os
import os.path
import sys
import logging
import subprocess
import configparser
from debmetrics.graph_helper import time_series_graph
from debmetrics.config_reader import settings, read_config
from debmetrics.runner_helper import (db_delete_all, db_fetch, db_insert,
                                      handle_csv, pack, should_run)

pkg_dir = os.path.dirname(os.path.abspath(__file__))
read_config()

directory = settings['PULL_DIRECTORY']
man_dir = settings['MANIFEST_DIRECTORY']
graph_dir = settings['GRAPH_DIRECTORY']
graph_scripts_directory = settings['GRAPH_SCRIPTS_DIRECTORY']

if not os.path.isabs(directory):
    directory = os.path.join(pkg_dir, directory)
if not os.path.isabs(man_dir):
    man_dir = os.path.join(pkg_dir, man_dir)
if not os.path.isabs(graph_scripts_directory):
    graph_scripts_directory = os.path.join(pkg_dir, graph_scripts_directory)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def run():
    """The main function that runs the pull scripts and generates graphs."""
    for filename in os.listdir(directory):
        name, ext = os.path.splitext(filename)
        if ext == '.py' and not name == '__init__':
            manifest = configparser.RawConfigParser()
            manifest.read(os.path.join(man_dir, name + '.manifest'))
            t = manifest.get('script1', 'type')
            if t == 'pull':
                print(os.path.join(man_dir, name + '.manifest'))
                format = manifest.get('script1', 'format')
                if should_run(name+ext, manifest.get('script1', 'freq')):
                    try:
                        output = subprocess.check_output(os.path.join(
                            directory, filename))
                        if format == 'csv':
                            header, rows = handle_csv(output)
                        delete = manifest.getboolean('script1',
                                                     'delete_before_insert')
                        if delete:
                            db_delete_all(name)
                        db_insert(header, rows, name)
                    except subprocess.CalledProcessError:
                        msg = 'Failure calling process for pull script %s'
                        logger.error(msg, filename)
                    except KeyError:
                        msg = 'Error on %s, does the table in the db exist?'
                        logger.error(msg, name)
                else:
                    logger.error('Did not run pull script %s', filename)

    for filename in os.listdir(man_dir):
        name, ext = os.path.splitext(filename)
        if ext == '.manifest' and not '__init__' in name:
            try:
                table = name
                data, cols, _, _ = db_fetch(table)
                config = configparser.RawConfigParser()
                config.read(os.path.join(man_dir, table + '.manifest'))
                t = config.get('script1', 'type')
                graph_type = config.get('script1', 'graph_type')
                if t == 'pull':
                    if data:
                        if graph_type == 'default':
                            time_series_graph(table, data, cols)
                    if filename in os.listdir(graph_scripts_directory):
                        data = pack(data)
                        proc = subprocess.Popen([os.path.join(
                                                graph_scripts_directory,
                                                filename)],
                                                stdin=subprocess.PIPE)
                        out, err = proc.communicate(data)
                        if err:
                            logger.error('Failure with graph script for' +
                                         '%s: %s', table, err)
            except subprocess.CalledProcessError:
                logger.error('Failure calling process for graph script' +
                             'for %s', table)

if __name__ == '__main__':
    if not os.path.exists(graph_dir):
        os.makedirs(graph_dir)
    run()
    exit(0)
