"""This module reads config files"""

import ConfigParser

settings = dict()


def read_config(config_file):
    """Reads a config file, creating a dictionary from it.

    Keyword arguments:
    config -- The location of the config file
    """
    config = ConfigParser.RawConfigParser()
    config.read(config_file)
    settings['DB_URI'] = config.get('DB', 'DB_URI')

if __name__ == '__main__':
    read_config('.debmetrics.ini')
