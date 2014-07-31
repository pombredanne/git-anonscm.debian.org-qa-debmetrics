#! /usr/bin/python3

import sys
import csv
from urllib.request import urlopen
from bs4 import BeautifulSoup


def run():
    url = 'http://upsilon.cc/~zack/stuff/dpkg-v3/'
    soup = BeautifulSoup(urlopen(url))
    rows = soup.find_all('td')
    data = []
    ts = soup.find_all('tt')[0].string
    data.append(ts)
    for row in rows:
        data.append(row.string)
    writer = csv.writer(sys.stdout)
    writer.writerow(['ts', '1.0', '3.0 (native)', '3.0 (quilt)'])
    writer.writerow(data)
    sys.exit(0)

if __name__ == '__main__':
    run()
