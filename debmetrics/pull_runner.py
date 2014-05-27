#! /usr/bin/python

import os
import subprocess
import ConfigParser

config = ConfigParser.RawConfigParser()
config.read('.debmetrics.ini')
directory = config.get('manifest', 'DIRECTORY')


for filename in os.listdir(directory):
    name, ext = os.path.splitext(filename)
    if ext == '.py' and not name == '__init__':
        if not subprocess.call('./' + directory + '/' + filename, shell=False):
            print 'success'
        else:
            print 'failure'
