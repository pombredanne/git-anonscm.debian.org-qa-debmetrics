#!/usr/bin/python3

import sys
import csv
import datetime
import feedparser

def run():
    url = 'http://mentors.debian.net/packages/feed'
    feed = feedparser.parse(url)
    writer = csv.writer(sys.stdout)
    writer.writerow(['ts', 'packages'])
    today = '%s' % datetime.datetime.utcnow()
    writer.writerow([today, len(feed.entries)])
    exit(0)

if __name__ == '__main__':
    run()
