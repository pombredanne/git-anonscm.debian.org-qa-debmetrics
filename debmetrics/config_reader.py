"""This module reads config files"""

import configparser
import os

settings = dict()

ROOT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')

CONF_FILES = [
    os.path.join(ROOT_DIR, '.debmetrics.local.ini'),
    '/etc/debmetrics/debmetrics.ini'
    ]


def read_config():
    for conffile in CONF_FILES:
        if os.path.exists(conffile):
            return read_config_file(conffile)


def read_config_file(config_file):
    """Reads a config file, creating a dictionary from it.

    Keyword arguments:
    config_file -- The location of the config file
    """
    config = configparser.RawConfigParser()
    config.read(config_file)
    settings['SECRET_KEY'] = config.get('session', 'SECRET_KEY')
    settings['DB_URI'] = config.get('db', 'DB_URI')
    settings['MANIFEST_DIRECTORY'] = config.get('manifest', 'DIRECTORY')
    settings['PULL_DIRECTORY'] = config.get('pull_scripts', 'DIRECTORY')
    settings['GRAPH_SCRIPTS_DIRECTORY'] = config.get('graph_scripts',
                                                     'DIRECTORY')
    settings['TEST'] = config.getboolean('test', 'TEST')

if __name__ == '__main__':
    read_config()
