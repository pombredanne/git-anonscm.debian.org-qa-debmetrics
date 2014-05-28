"""This module reads config files"""

import ConfigParser

settings = dict()


def read_config(config_file):
    """Reads a config file, creating a dictionary from it.

    Keyword arguments:
    config_file -- The location of the config file
    """
    config = ConfigParser.RawConfigParser()
    config.read(config_file)
    settings['DB_URI'] = config.get('db', 'DB_URI')
    settings['PSYCOPG2_DB_STRING'] = config.get('db', 'PSYCOPG2_DB_STRING')
    settings['DIRECTORY'] = config.get('manifest', 'DIRECTORY')

if __name__ == '__main__':
    read_config('.debmetrics.ini')
