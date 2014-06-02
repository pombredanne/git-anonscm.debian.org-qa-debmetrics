#!/usr/bin/python
import os
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/debmetrics/")
os.chdir("/var/www/debmetrics/debmetrics/")

from debmetrics import app as application
