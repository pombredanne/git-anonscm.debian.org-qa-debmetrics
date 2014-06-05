#! /usr/bin/python

import sys
import json
import csv
import urllib2
import datetime


def run():
    url = 'https://upsilon.cc/~zack/stuff/vcs-usage/usage.json'
    j = json.load(urllib2.urlopen(url))
    j = j['values'][0]
    writer = csv.writer(sys.stdout)
    writer.writerow(['ts', 'svn', 'darcs', 'git', 'bzr', 'using_vcs', 'cvs',
                     'mtn', 'total', 'arch', 'hg'])
    today = "TIMESTAMP '%s'" % datetime.datetime.utcnow()
    writer.writerow([today, j['svn'], j['darcs'],
                    j['git'], j['bzr'], j['using_vcs'], j['cvs'], j['mtn'],
                    j['total'], j['arch'], j['hg']])
    sys.exit(0)


if __name__ == '__main__':
    run()
