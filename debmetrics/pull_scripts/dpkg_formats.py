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
    writer.writerow(['ts', 'v1dot0', 'v3dot0_native', 'v3dot0_quilt'])
    writer.writerow(data)
    exit(0)

if __name__ == '__main__':
    run()
