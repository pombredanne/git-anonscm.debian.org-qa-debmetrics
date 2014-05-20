"""This module reads config files"""


settings = dict()


def read_config(config):
    """Reads a config file, creating a dictionary from it.

    Keyword arguments:
    config -- The location of the config file
    """
    f = open(config, 'r')
    for line in f:
        key = line.split(' = ')[0]
        val = line.split(' = ')[1][1:-2]
        settings[key] = val
    f.close()

if __name__ == '__main__':
    read_config('.debmetrics.cfg')
