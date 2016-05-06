#!/usr/bin/python3
import os
import sys
import logging
logging.basicConfig(stream=sys.stderr)

from debmetrics.app import app as application
