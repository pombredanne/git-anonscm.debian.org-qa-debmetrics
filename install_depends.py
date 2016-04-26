#! /usr/bin/python3

import os
import os.path
import subprocess
import configparser
from debmetrics.config_reader import settings, read_config

pkg_dir = os.path.dirname(os.path.abspath(__file__))
read_config()

man_dir = settings['MANIFEST_DIRECTORY']

if not os.path.isabs(man_dir):
    man_dir = os.path.join(pkg_dir, man_dir)

config = configparser.RawConfigParser({'depends': ''})
for manifest in os.listdir(man_dir):
    config.read(os.path.join(man_dir, manifest))
    depends = config.get('script1', 'depends')
    depends = depends.split(', ')
    for depend in depends:
        if depend:
            subprocess.check_call(['apt-get', 'install', '-y', depend])
