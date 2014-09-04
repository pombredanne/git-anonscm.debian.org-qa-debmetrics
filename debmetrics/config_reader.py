"""This module reads config files"""

import configparser

settings = dict()


def read_config(config_file):
    """Reads a config file, creating a dictionary from it.

    Keyword arguments:
    config_file -- The location of the config file
    """
    config = configparser.RawConfigParser()
    config.read(config_file)
    settings['DB_URI'] = config.get('db', 'DB_URI')
    settings['MANIFEST_DIRECTORY'] = config.get('manifest', 'DIRECTORY')
    settings['PULL_DIRECTORY'] = config.get('pull_scripts', 'DIRECTORY')
    settings['GRAPH_SCRIPTS_DIRECTORY'] = config.get('graph_scripts',
                                                     'DIRECTORY')
    settings['TEST'] = config.getboolean('test', 'TEST')

if __name__ == '__main__':
    read_config('../.debmetrics.ini')
