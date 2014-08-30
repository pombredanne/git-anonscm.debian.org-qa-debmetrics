#! /usr/bin/python3

import sys
import csv
from urllib.request import urlopen
import datetime
from bs4 import BeautifulSoup


def run():
    url = 'http://upsilon.cc/~zack/stuff/dh-vs-cdbs/'
    soup = BeautifulSoup(urlopen(url))
    cols = soup.find_all('td')[1::2]
    dh = cols[0].string.strip()
    cdbs = cols[1].string.strip()
    writer = csv.writer(sys.stdout)
    writer.writerow(['ts', 'debhelper_grtr_7', 'cdbs'])
    today = '%s' % datetime.datetime.utcnow()
    writer.writerow([today, dh, cdbs])
    exit(0)

if __name__ == '__main__':
    run()
