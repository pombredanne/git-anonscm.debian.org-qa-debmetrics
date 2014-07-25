#!/usr/bin/python3
import os
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, "/var/www/debmetrics/")
os.chdir("/var/www/debmetrics/")

from app import app as application
